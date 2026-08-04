"""  
VISTOR Ingest Web App  
  
A local, single-page drag-and-drop UI over IngestSession. Runs on  
127.0.0.1 only. Routes:  
  
    GET  /          -> the drop page  
    POST /preview   -> {url, media_type} -> {record, candidates}  
    POST /choose    -> {url, tmdb_id, media_type} -> {record}  
    POST /commit    -> {record, download, overwrite} -> ingest report  
  
The Type dropdown (Auto / Movie / MusicVideo / Episode / Commercial) flows  
through /preview as overrides["type"]. RecordBuilder treats an explicit type  
as sticky Layer-1, which resolves the type BEFORE enrichment so the correct  
authoritative backend (TMDB for movies/TV, MusicBrainz for music) is chosen.  
"Auto" sends an empty type and lets the classifier decide.  
"""  
  
from flask import Flask, request, jsonify  
  
from ingest.ingest_session import IngestSession  
  
app = Flask(__name__)  
_session = IngestSession()  
  
_PAGE = """<!doctype html>  
<html><head><meta charset="utf-8"><title>VISTOR - Add Media</title>  
<style>  
 body{font-family:system-ui,Arial,sans-serif;margin:0;background:#111;color:#eee}  
 .wrap{max-width:980px;margin:0 auto;padding:24px}  
 #drop{border:2px dashed #666;border-radius:10px;padding:40px;text-align:center;color:#aaa}  
 #drop.hover{border-color:#4ea1ff;color:#4ea1ff}  
 input[type=text]{width:100%;padding:10px;margin-top:10px;background:#1c1c1c;color:#eee;border:1px solid #444;border-radius:6px}  
 select{padding:9px;margin-top:10px;background:#1c1c1c;color:#eee;border:1px solid #444;border-radius:6px}  
 .cols{display:flex;gap:20px;margin-top:20px}  
 .card{flex:2;background:#1a1a1a;border:1px solid #333;border-radius:10px;padding:16px}  
 .side{flex:1;background:#1a1a1a;border:1px solid #333;border-radius:10px;padding:16px}  
 .cover{width:100%;border-radius:6px;background:#000}  
 .chip{display:flex;gap:10px;align-items:center;padding:8px;border:1px solid #333;border-radius:8px;margin-bottom:8px;cursor:pointer}  
 .chip:hover{border-color:#4ea1ff}  
 .chip img{width:46px;border-radius:4px}  
 button{padding:10px 16px;border:0;border-radius:6px;cursor:pointer;font-weight:600}  
 .ok{background:#2e7d32;color:#fff}.no{background:#7d2e2e;color:#fff}  
 label{font-size:13px;color:#aaa}  
 pre{white-space:pre-wrap;background:#000;padding:10px;border-radius:6px;max-height:220px;overflow:auto}  
</style></head><body><div class="wrap">  
 <h2>VISTOR - Add Media</h2>  
 <div id="drop">Drag a link here, or paste it below</div>  
 <input id="url" type="text" placeholder="https://youtu.be/...">  
 <div style="margin-top:10px">  
   <label>Type  
     <select id="mtype">  
       <option value="">Auto (detect)</option>  
       <option value="Movie">Movie</option>  
       <option value="MusicVideo">MusicVideo</option>  
       <option value="Episode">Episode</option>  
       <option value="Commercial">Commercial</option>  
     </select>  
   </label>  
   <button class="ok" onclick="preview()">Preview</button>  
   <label style="margin-left:10px"><input type="checkbox" id="dl" checked> download now</label>  
   <label style="margin-left:10px"><input type="checkbox" id="ow"> overwrite if it already exists</label>  
 </div>  
 <div class="cols">  
  <div class="card" id="card" style="display:none">  
    <img class="cover" id="cover">  
    <h3 id="t"></h3>  
    <div id="meta"></div>  
    <p id="desc"></p>  
    <label>ID (edit to avoid dedupe skip)</label>  
    <input id="rid" type="text">  
    <div style="margin-top:12px">  
      <button class="ok" onclick="commit()">Confirm &amp; add</button>  
      <button class="no" onclick="cancel()">Cancel</button>  
    </div>  
  </div>  
  <div class="side" id="side" style="display:none">  
    <h4>Did you mean...?</h4>  
    <div id="cands"></div>  
  </div>  
 </div>  
 <pre id="log"></pre>  
</div>  
<script>  
let RECORD=null, URL_="";  
const drop=document.getElementById('drop');  
['dragover'].forEach(e=>drop.addEventListener(e,ev=>{ev.preventDefault();drop.classList.add('hover')}));  
['dragleave','drop'].forEach(e=>drop.addEventListener(e,ev=>{ev.preventDefault();drop.classList.remove('hover')}));  
drop.addEventListener('drop',ev=>{  
  const t=ev.dataTransfer.getData('text')||ev.dataTransfer.getData('text/uri-list');  
  if(t){document.getElementById('url').value=t.trim();preview();}  
});  
function log(m){document.getElementById('log').textContent=(typeof m==='string')?m:JSON.stringify(m,null,2);}  
async function post(u,b){const r=await fetch(u,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});return r.json();}  
function show(rec,cands){  
  RECORD=rec;  
  document.getElementById('card').style.display='block';  
  document.getElementById('cover').src=rec.poster_url||'';  
  document.getElementById('t').textContent=rec.title||'';  
  document.getElementById('meta').textContent=(rec.type||'')+' - '+(rec.release_year||'?')+' - '+((rec.genres||[]).join(', ')||'no genres');  
  document.getElementById('desc').textContent=rec.description||'';  
  document.getElementById('rid').value=rec.id||'';  
  const side=document.getElementById('side'),box=document.getElementById('cands');  
  box.innerHTML='';  
  if(cands&&cands.length){side.style.display='block';  
    cands.forEach(c=>{const d=document.createElement('div');d.className='chip';  
      d.innerHTML=(c.poster_url?'<img src="'+c.poster_url+'">':'')+'<span>'+c.title+' ('+(c.release_year||'?')+')</span>';  
      d.onclick=()=>choose(c.tmdb_id,c.media_type);box.appendChild(d);});  
  } else {side.style.display='none';}  
}  
async function preview(){URL_=document.getElementById('url').value.trim();if(!URL_)return;  
  const mt=document.getElementById('mtype').value;  
  log('Building preview...');const r=await post('/preview',{url:URL_,media_type:mt});  
  if(r.error){log(r.error);return;}show(r.record,r.candidates);log('Preview ready. Pick a "did you mean" match if the cover/year is wrong.');}  
async function choose(id,mt){log('Fetching chosen match...');const r=await post('/choose',{url:URL_,tmdb_id:id,media_type:mt});  
  if(r.error){log(r.error);return;}RECORD=r.record;show(r.record,null);document.getElementById('side').style.display='block';}  
async function commit(){if(!RECORD)return;RECORD.id=document.getElementById('rid').value.trim();  
  log('Committing...');const r=await post('/commit',{record:RECORD,download:document.getElementById('dl').checked,overwrite:document.getElementById('ow').checked});  
  log(r);}  
function cancel(){RECORD=null;document.getElementById('card').style.display='none';  
  document.getElementById('side').style.display='none';log('Cancelled. Nothing was written.');}  
</script></body></html>"""  
  
  
@app.route("/")  
def index():  
    return _PAGE  
  
  
@app.route("/preview", methods=["POST"])  
def preview():  
    data = request.get_json(force=True) or {}  
    url = data.get("url", "").strip()  
    media_type = (data.get("media_type") or "").strip()  
    if not url:  
        return jsonify({"error": "No URL provided."})  
    try:  
        overrides = {"type": media_type} if media_type else None  
        record = _session.build(url, overrides=overrides)  
        cands = _session.candidates(record.get("title", ""), record.get("type"))  
        return jsonify({"record": record, "candidates": cands})  
    except Exception as exc:  # noqa: BLE001  
        return jsonify({"error": f"Preview failed: {exc!r}"})  
  
  
@app.route("/choose", methods=["POST"])  
def choose():  
    data = request.get_json(force=True) or {}  
    url = data.get("url", "").strip()  
    tmdb_id = data.get("tmdb_id")  
    media_type = data.get("media_type", "Movie")  
    if not url or not tmdb_id:  
        return jsonify({"error": "url and tmdb_id are required."})  
    try:  
        record = _session.build_from_tmdb(url, tmdb_id, media_type=media_type)  
        return jsonify({"record": record})  
    except Exception as exc:  # noqa: BLE001  
        return jsonify({"error": f"Choose failed: {exc!r}"})  
  
  
@app.route("/commit", methods=["POST"])  
def commit():  
    data = request.get_json(force=True) or {}  
    record = data.get("record")  
    download = bool(data.get("download", True))  
    overwrite = bool(data.get("overwrite", False))  
    if not record:  
        return jsonify({"error": "No record to commit."})  
    try:  
        report = _session.commit(record, download=download, overwrite=overwrite)  
        return jsonify(report)  
    except Exception as exc:  # noqa: BLE001  
        return jsonify({"error": f"Commit failed: {exc!r}"})  
  
  
def run():  
    app.run(host="127.0.0.1", port=5000, debug=False)