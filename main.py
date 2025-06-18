import streamlit as st
import os
import subprocess
from yt_dlp import YoutubeDL
import uuid

# --- Diccionario de Textos para Internacionalización (i18n) ---
TEXTS = {
    "en": {
        "app_title": "🎬 YouTube Video & Music Mixer",
        "app_description": "Enter YouTube URLs to generate a video with two audio tracks.",
        "main_video_header": "Main Video",
        "main_video_url_input": "🔗 Main Video URL:",
        "main_video_placeholder_info": "Enter the main video URL to preview it here.",
        "main_video_invalid_url_warning": "This does not seem to be a valid YouTube URL for the main video. Please check.",
        "music_track_header": "Music Track",
        "music_url_input": "🎶 Music Video URL:",
        "music_placeholder_info": "Enter the music URL to preview it here.",
        "music_invalid_url_warning": "This does not seem to be a valid YouTube URL for the music track. Please check.",
        "start_music_time_input": "⏱️ Start music from (HH:MM:SS format)",
        "output_duration_input": "⏳ Final video duration (seconds, optional)",
        "output_duration_help": "If left empty, the video will be the same duration as the main video.",
        "volume_settings_header": "**Volume Settings:**",
        "main_video_volume_slider": "🔊 Main video audio volume",
        "music_volume_slider": "🎵 Music audio volume",
        "volume_help_text": "1.0 is original volume. Less than 1.0 lowers volume, more than 1.0 increases it.",
        "process_button": "🎛️ Process",
        "warning_enter_both_urls": "Please enter both URLs.",
        "error_invalid_youtube_urls": "Please enter valid YouTube URLs for both fields.",
        "spinner_downloading_processing": "Downloading and processing... This may take a few minutes.",
        "info_downloading_main_video": "Downloading main video...",
        "info_downloading_music_audio": "Downloading music audio...",
        "info_mixing_audio_generating_video": "Mixing audios and generating video...",
        "success_video_generated": "Video generated successfully!",
        "error_ffmpeg_processing": "Oops! An error occurred while processing the video with FFmpeg.",
        "error_details": "Error details:",
        "info_check_urls_ffmpeg": "Please verify that the URLs are valid and that FFmpeg is correctly installed.",
        "download_button": "📥 Download mixed video",
        "error_unexpected": "An unexpected error occurred:",
        "warning_invalid_duration": "The entered duration is not a valid number. The main video's duration will be used.",
        "support_header": "Support Us!",
        "support_text": "If you like this tool, consider supporting our work:",
        "buy_me_a_coffee_text": "Buy Me a Coffee",
    },
    "es": {
        "app_title": "🎬 Mezclador de Video y Música de YouTube",
        "app_description": "Ingresa URLs de YouTube para generar un video con dos pistas de audio.",
        "main_video_header": "Video Principal",
        "main_video_url_input": "🔗 URL del video principal:",
        "main_video_placeholder_info": "Ingresa la URL del video principal para previsualizarlo aquí.",
        "main_video_invalid_url_warning": "Parece que no es una URL válida de YouTube para el video principal. Por favor, verifica.",
        "music_track_header": "Pista de Música",
        "music_url_input": "🎶 URL del video de música:",
        "music_placeholder_info": "Ingresa la URL de la música para previsualizarla aquí.",
        "music_invalid_url_warning": "Parece que no es una URL válida de YouTube para la pista de música. Por favor, verifica.",
        "start_music_time_input": "⏱️ Comenzar música desde (formato HH:MM:SS)",
        "output_duration_input": "⏳ Duración del video final (segundos, opcional)",
        "output_duration_help": "Si se deja vacío, el video durará lo mismo que el video principal.",
        "volume_settings_header": "**Ajustes de Volumen:**",
        "main_video_volume_slider": "🔊 Volumen del audio del video principal",
        "music_volume_slider": "🎵 Volumen del audio de la música",
        "volume_help_text": "1.0 es el volumen original. Menos de 1.0 baja el volumen, más de 1.0 lo sube.",
        "process_button": "🎛️ Procesar",
        "warning_enter_both_urls": "Por favor ingresá ambas URLs.",
        "error_invalid_youtube_urls": "Por favor, ingresa URLs válidas de YouTube para ambos campos.",
        "spinner_downloading_processing": "Descargando y procesando... Esto puede tardar unos minutos.",
        "info_downloading_main_video": "Descargando video principal...",
        "info_downloading_music_audio": "Descargando audio de música...",
        "info_mixing_audio_generating_video": "Mezclando audios y generando video...",
        "success_video_generated": "¡Video generado con éxito!",
        "error_ffmpeg_processing": "¡Oops! Ocurrió un error al procesar el video con FFmpeg.",
        "error_details": "Detalles del error:",
        "info_check_urls_ffmpeg": "Verificá que las URLs sean válidas y que FFmpeg esté correctamente instalado.",
        "download_button": "📥 Descargar video mezclado",
        "error_unexpected": "Se produjo un error inesperado:",
        "warning_invalid_duration": "La duración ingresada no es un número válido. Se usará la duración del video principal.",
        "support_header": "¡Apóyanos!",
        "support_text": "Si te gusta esta herramienta, considera apoyar nuestro trabajo:",
        "buy_me_a_coffee_text": "Invítame un café",
    },
    "zh": { # Mandarín (simplificado)
        "app_title": "🎬 YouTube 视频和音乐混合器",
        "app_description": "输入 YouTube 链接以生成带有两条音轨的视频。",
        "main_video_header": "主视频",
        "main_video_url_input": "🔗 主视频链接:",
        "main_video_placeholder_info": "在此输入主视频链接以进行预览。",
        "main_video_invalid_url_warning": "这似乎不是主视频的有效 YouTube 链接。请检查。",
        "music_track_header": "音乐音轨",
        "music_url_input": "🎶 音乐视频链接:",
        "music_placeholder_info": "在此输入音乐链接以进行预览。",
        "music_invalid_url_warning": "这似乎不是音乐音轨的有效 YouTube 链接。请检查。",
        "start_music_time_input": "⏱️ 音乐开始时间 (HH:MM:SS 格式)",
        "output_duration_input": "⏳ 最终视频时长 (秒，可选)",
        "output_duration_help": "如果留空，视频时长将与主视频相同。",
        "volume_settings_header": "**音量设置：**",
        "main_video_volume_slider": "🔊 主视频音频音量",
        "music_volume_slider": "🎵 音乐音频音量",
        "volume_help_text": "1.0 为原始音量。小于 1.0 降低音量，大于 1.0 提高音量。",
        "process_button": "🎛️ 处理",
        "warning_enter_both_urls": "请输入两个链接。",
        "error_invalid_youtube_urls": "请输入有效的 YouTube 链接。",
        "spinner_downloading_processing": "正在下载和处理... 这可能需要几分钟。",
        "info_downloading_main_video": "正在下载主视频...",
        "info_downloading_music_audio": "正在下载音乐音频...",
        "info_mixing_audio_generating_video": "正在混合音频并生成视频...",
        "success_video_generated": "视频生成成功！",
        "error_ffmpeg_processing": "哎呀！使用 FFmpeg 处理视频时发生错误。",
        "error_details": "错误详情：",
        "info_check_urls_ffmpeg": "请验证链接是否有效以及 FFmpeg 是否正确安装。",
        "download_button": "📥 下载混合视频",
        "error_unexpected": "发生意外错误：",
        "warning_invalid_duration": "输入的时长不是有效数字。将使用主视频的时长。",
        "support_header": "支持我们！",
        "support_text": "如果您喜欢此工具，请考虑支持我们的工作：",
        "buy_me_a_coffee_text": "请我喝杯咖啡",
    },
    "fr": { # Francés
        "app_title": "🎬 Mixeur Vidéo & Musique YouTube",
        "app_description": "Entrez les URL YouTube pour générer une vidéo avec deux pistes audio.",
        "main_video_header": "Vidéo Principale",
        "main_video_url_input": "🔗 URL de la vidéo principale :",
        "main_video_placeholder_info": "Entrez l'URL de la vidéo principale pour la prévisualiser ici.",
        "main_video_invalid_url_warning": "Cela ne semble pas être une URL YouTube valide pour la vidéo principale. Veuillez vérifier.",
        "music_track_header": "Piste Musicale",
        "music_url_input": "🎶 URL de la vidéo musicale :",
        "music_placeholder_info": "Entrez l'URL de la musique pour la prévisualiser ici.",
        "music_invalid_url_warning": "Cela ne semble pas être une URL YouTube valide pour la piste musicale. Veuillez vérifier.",
        "start_music_time_input": "⏱️ Commencer la musique à partir de (format HH:MM:SS)",
        "output_duration_input": "⏳ Durée finale de la vidéo (secondes, optionnel)",
        "output_duration_help": "Si laissé vide, la vidéo aura la même durée que la vidéo principale.",
        "volume_settings_header": "**Paramètres de Volume :**",
        "main_video_volume_slider": "🔊 Volume audio de la vidéo principale",
        "music_volume_slider": "🎵 Volume audio de la musique",
        "volume_help_text": "1.0 est le volume original. Moins de 1.0 diminue le volume, plus de 1.0 l'augmente.",
        "process_button": "🎛️ Traiter",
        "warning_enter_both_urls": "Veuillez entrer les deux URL.",
        "error_invalid_youtube_urls": "Veuillez entrer des URL YouTube valides pour les deux champs.",
        "spinner_downloading_processing": "Téléchargement et traitement en cours... Cela peut prendre quelques minutes.",
        "info_downloading_main_video": "Téléchargement de la vidéo principale...",
        "info_downloading_music_audio": "Téléchargement de l'audio musical...",
        "info_mixing_audio_generating_video": "Mixage des audios et génération de la vidéo...",
        "success_video_generated": "Vidéo générée avec succès !",
        "error_ffmpeg_processing": "Oups ! Une erreur est survenue lors du traitement de la vidéo avec FFmpeg.",
        "error_details": "Détails de l'erreur :",
        "info_check_urls_ffmpeg": "Veuillez vérifier que les URL sont valides et que FFmpeg est correctement installé.",
        "download_button": "📥 Télécharger la vidéo mixée",
        "error_unexpected": "Une erreur inattendue est survenue :",
        "warning_invalid_duration": "La durée saisie n'est pas un nombre valide. La durée de la vidéo principale sera utilisée.",
        "support_header": "Soutenez-nous !",
        "support_text": "Si vous aimez cet outil, pensez à soutenir notre travail :",
        "buy_me_a_coffee_text": "Offrez-moi un café",
    },
    "pt": { # Portugués
        "app_title": "🎬 Misturador de Vídeo e Música do YouTube",
        "app_description": "Insira URLs do YouTube para gerar um vídeo com duas faixas de áudio.",
        "main_video_header": "Vídeo Principal",
        "main_video_url_input": "🔗 URL do vídeo principal:",
        "main_video_placeholder_info": "Digite a URL do vídeo principal para visualizá-lo aqui.",
        "main_video_invalid_url_warning": "Esta não parece ser uma URL válida do YouTube para o vídeo principal. Por favor, verifique.",
        "music_track_header": "Faixa de Música",
        "music_url_input": "🎶 URL do vídeo de música:",
        "music_placeholder_info": "Digite a URL da música para visualizá-la aqui.",
        "music_invalid_url_warning": "Esta não parece ser uma URL válida do YouTube para a faixa de música. Por favor, verifique.",
        "start_music_time_input": "⏱️ Iniciar música de (formato HH:MM:SS)",
        "output_duration_input": "⏳ Duração final do vídeo (segundos, opcional)",
        "output_duration_help": "Se deixado em branco, o vídeo terá a mesma duração do vídeo principal.",
        "volume_settings_header": "**Configurações de Volume:**",
        "main_video_volume_slider": "🔊 Volume de áudio do vídeo principal",
        "music_volume_slider": "🎵 Volume de áudio da música",
        "volume_help_text": "1.0 é o volume original. Menos de 1.0 diminui o volume, mais de 1.0 aumenta.",
        "process_button": "🎛️ Processar",
        "warning_enter_both_urls": "Por favor, insira ambas as URLs.",
        "error_invalid_youtube_urls": "Por favor, insira URLs válidas do YouTube para ambos os campos.",
        "spinner_downloading_processing": "Baixando e processando... Isso pode levar alguns minutos.",
        "info_downloading_main_video": "Baixando vídeo principal...",
        "info_downloading_music_audio": "Baixando áudio de música...",
        "info_mixing_audio_generating_video": "Misturando áudios e gerando vídeo...",
        "success_video_generated": "Vídeo gerado com sucesso!",
        "error_ffmpeg_processing": "Oops! Ocorreu um erro ao processar o vídeo com FFmpeg.",
        "error_details": "Detalhes do erro:",
        "info_check_urls_ffmpeg": "Verifique se as URLs são válidas e se o FFmpeg está instalado corretamente.",
        "download_button": "📥 Baixar vídeo mixado",
        "error_unexpected": "Ocorreu um erro inesperado:",
        "warning_invalid_duration": "A duração inserida não é um número válido. A duração do vídeo principal será usada.",
        "support_header": "Apoie-nos!",
        "support_text": "Se você gostou desta ferramenta, considere apoiar nosso trabalho:",
        "buy_me_a_coffee_text": "Compre-me um café",
    },
}

# --- Inicialización del Idioma ---
# Define los idiomas disponibles y su mapeo a los códigos internos
LANGUAGES = {
    "English": "en",
    "Español": "es",
    "Mandarin (简体)": "zh",
    "Français": "fr",
    "Português": "pt",
}

# Establece el idioma predeterminado si no está en la sesión
if 'current_lang' not in st.session_state:
    st.session_state.current_lang = "en" # Inglés como default

# Selector de idioma en la barra lateral
st.sidebar.title("Language / Idioma")
selected_lang_name = st.sidebar.selectbox(
    "Select Language:",
    options=list(LANGUAGES.keys()),
    index=list(LANGUAGES.values()).index(st.session_state.current_lang)
)

# Actualiza el idioma si el usuario lo cambia
if LANGUAGES[selected_lang_name] != st.session_state.current_lang:
    st.session_state.current_lang = LANGUAGES[selected_lang_name]
    st.rerun() # Rerun la aplicación para aplicar el nuevo idioma

# Obtener los textos para el idioma actual
current_texts = TEXTS[st.session_state.current_lang]

# --- Aplicación Streamlit ---
st.title(current_texts["app_title"])
st.markdown(current_texts["app_description"])

# --- ENTRADAS DE URL Y PREVISUALIZACIÓN ---

# Contenedor para el video principal
st.subheader(current_texts["main_video_header"])
video_url = st.text_input(current_texts["main_video_url_input"], key="video_url_input")
if video_url:
    # Una validación de URL muy básica para st.video.
    # yt-dlp es más robusto en la descarga.
    if "youtube.com/watch" in video_url or "youtu.be/" in video_url: # Changed to more common YouTube URL patterns
        st.video(video_url)
    else:
        st.warning(current_texts["main_video_invalid_url_warning"])
else:
    st.info(current_texts["main_video_placeholder_info"])

st.markdown("---")

# Contenedor para la música
st.subheader(current_texts["music_track_header"])
music_url = st.text_input(current_texts["music_url_input"], key="music_url_input")
if music_url:
    if "youtube.com/watch" in music_url or "youtu.be/" in music_url: # Changed to more common YouTube URL patterns
        st.video(music_url)
    else:
        st.warning(current_texts["music_invalid_url_warning"])
else:
    st.info(current_texts["music_placeholder_info"])

st.markdown("---")

# --- AJUSTES DE TIEMPO Y VOLUMEN ---
start_time_str = st.text_input(current_texts["start_music_time_input"], value="00:00:00")
duration_str = st.text_input(
    current_texts["output_duration_input"],
    help=current_texts["output_duration_help"]
)

st.markdown("---")
st.write(current_texts["volume_settings_header"])

main_volume = st.slider(
    current_texts["main_video_volume_slider"],
    min_value=0.0,
    max_value=5.0,
    value=1.0,
    step=0.1,
    help=current_texts["volume_help_text"]
)

music_volume = st.slider(
    current_texts["music_volume_slider"],
    min_value=0.0,
    max_value=5.0,
    value=1.0,
    step=0.1,
    help=current_texts["volume_help_text"]
)
st.markdown("---")

# --- Botón de Procesar ---

if st.button(current_texts["process_button"]):
    if not video_url or not music_url:
        st.warning(current_texts["warning_enter_both_urls"])
    elif not (("youtube.com/watch" in video_url or "youtu.be/" in video_url) and \
              ("youtube.com/watch" in music_url or "youtu.be/" in music_url)):
        st.error(current_texts["error_invalid_youtube_urls"])
    else:
        with st.spinner(current_texts["spinner_downloading_processing"]):
            unique_id = str(uuid.uuid4())[:8]
            video_file = f"main_video_{unique_id}.mp4"
            music_file = f"music_audio_{unique_id}.m4a"
            output_file = f"output_mixed_video_{unique_id}.mp4"

            try:
                # Verifica si picaron.txt está presente
                cookie_file = "picaron.txt"
                use_cookies = os.path.exists(cookie_file)

                # --- VIDEO ---
                ydl_opts_video = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                    'outtmpl': video_file,
                    'merge_output_format': 'mp4',
                    'quiet': True,
                    'no_warnings': True,
                    'ignoreerrors': True,
                }
                if use_cookies:
                    ydl_opts_video['cookiefile'] = cookie_file

                with YoutubeDL(ydl_opts_video) as ydl:
                    st.info(current_texts["info_downloading_main_video"])
                    result = ydl.download([video_url])
                    if result != 0 or not os.path.exists(video_file):
                        raise RuntimeError("Video principal no pudo descargarse. Puede requerir verificación CAPTCHA.")

                # --- MÚSICA ---
                ydl_opts_music = {
                    'format': 'bestaudio[ext=m4a]/bestaudio',
                    'outtmpl': music_file,
                    'quiet': True,
                    'no_warnings': True,
                    'ignoreerrors': True,
                }
                if use_cookies:
                    ydl_opts_music['cookiefile'] = cookie_file

                with YoutubeDL(ydl_opts_music) as ydl:
                    st.info(current_texts["info_downloading_music_audio"])
                    result = ydl.download([music_url])
                    if result != 0 or not os.path.exists(music_file):
                        raise RuntimeError("El audio de música no pudo descargarse. Puede requerir verificación CAPTCHA.")

                # --- Mezcla con ffmpeg ---
                st.info(current_texts["info_mixing_audio_generating_video"])

                command = [
                    "ffmpeg",
                    "-i", video_file,
                    "-ss", start_time_str,
                    "-i", music_file,
                    "-filter_complex",
                    f"[0:a]volume={main_volume}[a0];[1:a]volume={music_volume}[a1];[a0][a1]amerge=inputs=2[a]",
                    "-map", "0:v",
                    "-map", "[a]",
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-ac", "2",
                    "-shortest",
                    "-y"
                ]

                if duration_str:
                    try:
                        duration_seconds = float(duration_str)
                        command.extend(["-t", str(duration_seconds)])
                    except ValueError:
                        st.warning(current_texts["warning_invalid_duration"])

                command.append(output_file)

                process = subprocess.run(command, capture_output=True, text=True)

                if process.returncode != 0:
                    st.error(current_texts["error_ffmpeg_processing"])
                    st.exception(f"{current_texts['error_details']} {process.stderr}")
                    st.info(current_texts["info_check_urls_ffmpeg"])
                else:
                    st.success(current_texts["success_video_generated"])
                    st.video(output_file)
                    with open(output_file, "rb") as file:
                        st.download_button(current_texts["download_button"], file, file_name="video_con_audio_combinado.mp4")

            except Exception as e:
                st.error(f"{current_texts['error_unexpected']} {e}")
                st.info(current_texts["info_check_urls_ffmpeg"])
            finally:
                for f in [video_file, music_file, output_file]:
                    if os.path.exists(f):
                        os.remove(f)


# --- Sección de Apoyo (Buy Me a Coffee) ---
st.markdown("---")
st.subheader(current_texts["support_header"])
st.write(current_texts["support_text"])

st.markdown(
    f"""
    <a href="https://www.buymeacoffee.com/jardouin" target="_blank">
        <img src="https://img.buymeacoffee.com/button-api/?text={current_texts['buy_me_a_coffee_text']}&slug=tu_nombre_de_usuario&button_colour=FFDD00&font_colour=000000&font_family=Inter&text_size=16&text_color=000000&outline_color=000000&coffee_text=Café" />
    </a>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
