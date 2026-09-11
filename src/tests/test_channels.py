"""  
VISTOR Channel Config Tests  
  
Validates ChannelConfigs/channels.json against the controlled genre  
vocabulary and the Audience enum so channel-to-media auto-discovery can  
actually fire. Offline-safe. Run standalone: python src/tests/test_channels.py  
"""  
  
import sys  
from pathlib import Path  
  
sys.path.append(str(Path(__file__).resolve().parent.parent))  
  
from channel.channel_loader import ChannelLoader  
from metadata.enums.audience import Audience  
from metadata.services.metadata_population import MetadataPopulation  
  
print("\n=== Testing Channel Config Integrity ===")  
  
config_path = Path(__file__).resolve().parents[2] / "ChannelConfigs" / "channels.json"  
  
loader = ChannelLoader(config_path=config_path)  
loader.load()  
channels = loader.get_channels()  
assert channels, "No channels loaded from channels.json"  
  
genre_names = {g.get_name().lower() for g in MetadataPopulation().create_genres()}  
audience_names = {member.name.lower() for member in Audience}  
  
for channel in channels:  
    genre = (channel.get_primary_genre() or "").strip().lower()  
    assert genre in genre_names, (  
        f"Channel {channel.get_number()} '{channel.get_name()}' uses "  
        f"primary_genre '{channel.get_primary_genre()}' not in the genre vocabulary."  
    )  
  
    audience = (channel.get_target_audience() or "").strip().lower().replace(" ", "_")  
    assert audience in audience_names, (  
        f"Channel {channel.get_number()} '{channel.get_name()}' uses "  
        f"target_audience '{channel.get_target_audience()}' not in the Audience enum."  
    )  
  
    logo = channel.get_logo()  
    logo_filename = logo.rsplit("/", 1)[-1]  
    assert logo_filename == logo_filename.lower(), (  
        f"Channel {channel.get_number()} '{channel.get_name()}' logo filename "  
        f"'{logo_filename}' is not lowercase (case-sensitive filesystem risk)."  
    )  
  
print(f"Channel config verified ({len(channels)} channels).")  
print("\nChannel config tests passed.")