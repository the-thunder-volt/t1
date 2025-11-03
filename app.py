import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader", page_icon="🎥", layout="centered")

st.title("🎬 YouTube Downloader (Video + Audio)")
st.markdown("Download YouTube videos or extract audio using **yt-dlp** + Streamlit.")

# === User Input ===
url = st.text_input("📎 Enter YouTube URL (Video or Playlist):")
download_type = st.radio("Select Download Type:", ["Video (MP4)", "Audio (MP3)"])
download_button = st.button("🚀 Download")

# === Download Directory ===
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube(url, is_audio=False):
    """Download YouTube video or audio using yt-dlp"""
    ydl_opts = {
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "noplaylist": False,
        "quiet": True,
        "progress_hooks": [lambda d: st.session_state.update({"status": d})],
    }

    if is_audio:
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        ydl_opts.update({
            "format": "bv*+ba/b",
            "merge_output_format": "mp4",
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if is_audio:
            filename = os.path.splitext(filename)[0] + ".mp3"
        return filename


if download_button and url:
    st.info("🔍 Fetching video details... please wait.")
    try:
        is_audio = download_type == "Audio (MP3)"
        file_path = download_youtube(url, is_audio=is_audio)

        st.success("✅ Download complete!")
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            st.download_button(
                label=f"⬇️ Download {file_name}",
                data=f,
                file_name=file_name,
                mime="audio/mpeg" if is_audio else "video/mp4"
            )

    except Exception as e:
        st.error(f"❌ Error: {e}")
