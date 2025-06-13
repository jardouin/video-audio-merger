import streamlit as st
import os
import subprocess
from yt_dlp import YoutubeDL
import uuid

st.title("🎬 Mezclar video y música de YouTube")
st.markdown("Ingresa las URLs de YouTube y generá un video con dos pistas de audio.")

# --- ENTRADAS DE URL Y PREVISUALIZACIÓN ---

# Contenedor para el video principal
st.subheader("Video Principal")
video_url = st.text_input("🔗 URL del video principal:", key="video_url_input")
if video_url:
    # Validar que sea una URL de YouTube simple antes de intentar incrustar
    # NOTA: La validación "youtube.com/watch?v=" es incorrecta para URLs de YouTube directas.
    # Usaremos una validación más robusta o la omitimos si confiamos en yt-dlp
    if "youtube.com/watch" in video_url or "youtu.be/" in video_url:
        st.video(video_url)
    else:
        st.warning("Parece que no es una URL válida de YouTube para el video principal. Por favor, verifica.")
else:
    st.info("Ingresa la URL del video principal para previsualizarlo aquí.")

st.markdown("---")

# Contenedor para la música
st.subheader("Pista de Música")
music_url = st.text_input("🎶 URL del video de música:", key="music_url_input")
if music_url:
    # Validar que sea una URL de YouTube simple antes de intentar incrustar
    if "youtube.com/watch" in music_url or "youtu.be/" in music_url:
        st.video(music_url)
    else:
        st.warning("Parece que no es una URL válida de YouTube para la pista de música. Por favor, verifica.")
else:
    st.info("Ingresa la URL de la música para previsualizarla aquí.")

st.markdown("---")

# --- AJUSTES DE TIEMPO Y VOLUMEN ---
start_time_str = st.text_input("⏱️ Comenzar música desde (formato HH:MM:SS)", value="00:00:00")
duration_str = st.text_input("⏳ Duración del video final (segundos, opcional)", help="Si se deja vacío, el video durará lo mismo que el video principal.")

st.markdown("---") # Separador para organizar la interfaz
st.write("**Ajustes de Volumen:**")

main_volume = st.slider(
    "🔊 Volumen del audio del video principal",
    min_value=0.0,
    max_value=5.0,
    value=1.0,
    step=0.1,
    help="1.0 es el volumen original. Menos de 1.0 baja el volumen, más de 1.0 lo sube."
)

music_volume = st.slider(
    "🎵 Volumen del audio de la música",
    min_value=0.0,
    max_value=5.0,
    value=1.0,
    step=0.1,
    help="1.0 es el volumen original. Menos de 1.0 baja el volumen, más de 1.0 lo sube."
)
st.markdown("---")

# --- BOTÓN DE PROCESAR ---
if st.button("🎛️ Procesar"):
    if not video_url or not music_url:
        st.warning("Por favor ingresá ambas URLs.")
    # Validar URLs de YouTube de forma más genérica
    elif not ("youtube.com/watch" in video_url or "youtu.be/" in video_url) or \
         not ("youtube.com/watch" in music_url or "youtu.be/" in music_url):
        st.error("Por favor, ingresa URLs válidas de YouTube para ambos campos.")
    else:
        with st.spinner("Descargando y procesando... Esto puede tardar unos minutos."):
            unique_id = str(uuid.uuid4())[:8]
            video_file = f"main_video_{unique_id}.mp4"
            music_file = f"music_audio_{unique_id}.m4a"
            output_file = f"output_mixed_video_{unique_id}.mp4"

            try:
                # Descargar video principal (mejor calidad de video con mejor audio)
                ydl_opts_video = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                    'outtmpl': video_file,
                    'merge_output_format': 'mp4',
                    'quiet': True,
                    'no_warnings': True
                }
                with YoutubeDL(ydl_opts_video) as ydl:
                    st.info("Descargando video principal...")
                    ydl.download([video_url])

                # Descargar solo audio de música (mejor calidad de audio)
                ydl_opts_music = {
                    'format': 'bestaudio[ext=m4a]/bestaudio',
                    'outtmpl': music_file,
                    'quiet': True,
                    'no_warnings': True
                }
                with YoutubeDL(ydl_opts_music) as ydl:
                    st.info("Descargando audio de música...")
                    ydl.download([music_url])

                st.info("Mezclando audios y generando video...")

                # Comando FFmpeg para combinar audio original + música
                command = [
                    "ffmpeg",
                    "-i", video_file,
                    # Aquí es donde movemos -ss: justo antes de la entrada de la música
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

                # Si se especifica una duración, agregarla al comando FFmpeg
                if duration_str:
                    try:
                        duration_seconds = float(duration_str)
                        # -t debe ir justo antes del archivo de salida para aplicar a la duración total del output
                        command.extend(["-t", str(duration_seconds)])
                    except ValueError:
                        st.warning("La duración ingresada no es un número válido. Se usará la duración del video principal.")

                command.append(output_file) # Asegura que el archivo de salida es el último argumento

                process = subprocess.run(command, capture_output=True, text=True)

                if process.returncode != 0:
                    st.error(f"¡Oops! Ocurrió un error al procesar el video con FFmpeg.")
                    st.exception(f"Detalles del error: {process.stderr}")
                    st.info("Verificá que las URLs sean válidas y que FFmpeg esté correctamente instalado.")
                else:
                    st.success("¡Video generado con éxito!")

                    # Mostrar el video en la app de Streamlit
                    st.video(output_file)

                    # Botón de descarga
                    with open(output_file, "rb") as file:
                        st.download_button("📥 Descargar video mezclado", file, file_name="video_con_audio_combinado.mp4")

            except Exception as e:
                st.error(f"Se produjo un error inesperado: {e}")
                st.info("Asegurate de que las URLs de YouTube sean válidas y que el video no tenga restricciones de descarga.")
            finally:
                # Limpieza de archivos temporales
                for f in [video_file, music_file, output_file]:
                    if os.path.exists(f):
                        os.remove(f)
