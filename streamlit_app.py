import music21
from music21 import stream, note, chord, meter, key, tempo
import io
import base64
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

st.set_page_config(page_title="Track to Track AI", layout="wide")

st.title("🎵 Track to Track AI")
st.markdown("---")

# Sidebar
with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password")

genres = ["Pop", "Rock", "EDM", "Hip-Hop", "Bossa Nova", "Gospel", "Jazz", "Funk", "Samba", "Reggae"]
col1, col2 = st.columns(2)

with col1:
    genre = st.selectbox("Estilo", genres)
    bpm = st.slider("BPM", 60, 180, 120)
    section = st.selectbox("Seção", ["Intro", "Verso", "Refrão"])

if st.button("🎨 GERAR MIDI", type="primary") and api_key:
    with st.spinner("Gerando..."):
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
        prompt = PromptTemplate.from_template(
            "Sugira progressão {section} estilo {genre} BPM {bpm}"
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        idea = chain.run(section=section, genre=genre, bpm=bpm)
        
        score = stream.Score()
        s = stream.Part()
        m = stream.Measure()
        ch = chord.Chord(["C4","E4","G4"])
        ch.duration.quarterLength = 4
        m.append(ch)
        s.append(m)
        score.append(s)
        
        midi_buffer = io.BytesIO()
        score.write('midi', fp=midi_buffer)
        b64 = base64.b64encode(midi_buffer.getvalue()).decode()
        st.markdown(f'<a href="data:audio/midi;base64,{b64}" download="track.mid">📥 Download MIDI</a>', unsafe_allow_html=True)
        st.success("✅ Gerado!")
        st.text_area("Ideia IA:", idea)

st.markdown("**Feito com ❤️ para produtores**")
