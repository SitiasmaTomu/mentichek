import joblib
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import google.generativeai as genai

# Load the saved pipeline
pipeline = joblib.load('MLMentalHealth-v2.sav')

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        'Mental Health System',
        ['Home Page', 'Chat Bot', 'Articles'],
        icons=['activity', 'chat', 'book'],
        default_index=0
    )

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Home Page
if selected == 'Home Page':
    st.markdown("""
        <div style='text-align:center;'>
            <h1 style='color: #f75c5c;'>🧠 Selamat Datang di <span style='color:white;'>Menti Check</span></h1>
            <p style='color:#ccc; font-size:18px; max-width:700px; margin:auto;'>
                Aplikasi ini membantu Anda memahami kondisi kesehatan mental Anda dan memberikan arahan apakah perlu bantuan profesional. Cocok digunakan oleh pelajar dan mahasiswa.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center;'>Misi Kami</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#ccc;'>Diakui sebagai penyedia informasi kesehatan berkualitas yang transparan dan terpercaya.</p>", unsafe_allow_html=True)

    row1 = st.columns(2)
    row2 = st.columns(2)
    missions = [
        {
            "title": "Panduan yang Dapat Dipercaya",
            "image": "https://www.helpguide.org/wp-content/uploads/Frame-13794.png",
            "text": "Temukan informasi terpercaya tentang kesehatan mental dan kebugaran yang dapat Anda gunakan untuk membuat keputusan yang lebih baik."
        },
        {
            "title": "Keterampilan untuk Sukses Hidup",
            "image": "https://www.helpguide.org/wp-content/uploads/Frame-13795-1.png",
            "text": "Bangun keterampilan untuk mengelola emosi Anda, memperkuat hubungan, dan menghadapi situasi sulit."
        },
        {
            "title": "Strategi untuk Merasa Lebih Baik",
            "image": "https://www.helpguide.org/wp-content/uploads/Frame-13791.png",
            "text": "Pelajari cara meningkatkan kesehatan mental dan kesejahteraan Anda—dan bantu teman serta keluarga Anda melakukan hal yang sama."
        },
        {
            "title": "Dukungan yang Bisa Diandalkan",
            "image": "https://www.helpguide.org/wp-content/uploads/Frame-13793.png",
            "text": "Sebagai sumber daya daring gratis, kami hadir untuk Anda, siang atau malam, kapan pun Anda membutuhkan panduan, dorongan, atau dukungan."
        }
    ]

    for i, col in enumerate(row1 + row2):
        if i < len(missions):
            with col:
                st.image(missions[i]["image"], width=120)
                st.subheader(missions[i]["title"])
                st.write(missions[i]["text"])
        else:
            col.empty()

# Chat Bot
elif selected == 'Chat Bot':
    st.markdown("""
        <div style='text-align:center;'>
            <h1 style='color: #f75c5c;'>Apa Yang Bisa <span style='color:white;'> Hari Ini ? </span></h1>
            <p style='color:#ccc; font-size:18px; max-width:700px; margin:auto;'>
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.warning("⚠️ Catatan: Chatbot ini hanya melayani topik seputar kesehatan mental.")
    st.info("ℹ️ Disclaimer: Chatbot ini bukan pengganti tenaga profesional. Jika Anda mengalami krisis atau membutuhkan bantuan serius, segera hubungi psikolog atau layanan darurat.")

    def is_valid_topic(user_input):
        topik_diperbolehkan = ["depresi", "cemas", "burnout", "psikologi", "kesehatan mental", "overthinking", "suasana hati", "stres", "gangguan mental", "hai", "halo", "hallo", "hei"]
        return any(kata in user_input.lower() for kata in topik_diperbolehkan)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "user", "parts": ["Anda adalah konsultan medis di bidang kesehatan mental. Anda akan membantu pengguna dengan pertanyaan atau keluhan terkait kesehatan mental mereka. Jangan menjawab pertanyaan yang tidak relevan dengan kesehatan mental."]}
        ]

    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown("".join(message["parts"]))

    prompt = st.chat_input("Silakan ketik pertanyaan atau keluhan Anda di sini…")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "parts": [prompt]})

        with st.chat_message("assistant", avatar="👩🏻‍⚕️"):
            message_placeholder = st.empty()
            full_response = ""

            if is_valid_topic(prompt):
                chat = model.start_chat(history=st.session_state.messages)
                response = chat.send_message(prompt, stream=True)
                for chunk in response:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "model", "parts": [full_response]})
            else:
                full_response = "Maaf, saya hanya dapat membantu pertanyaan seputar kesehatan mental."
                message_placeholder.markdown(full_response)

# Articles
elif selected == 'Articles':
    st.markdown("""
        <div style='text-align:center;'>
            <h1 style='color: #f75c5c;'>Artikel <span style='color:white;'>Kesehatan Mental</span></h1>
            <p style='color:#ccc; font-size:18px; max-width:700px; margin:auto;'>
                Berikut adalah beberapa artikel yang dapat membantu Anda memahami lebih lanjut 
    tentang kesehatan mental dan cara mengelolanya:
            </p>
        </div>
    """, unsafe_allow_html=True)


    articles = [
        {
            "title": "Kesehatan Mental Bukan Sekedar Trend: Saatnya Serius Menata Dukungan Psikologis di Indonesia",
            "description": "Artikel opini yang menekankan bahwa kesadaran soal kesehatan mental di Indonesia belum diiringi dengan layanan yang memadai.",
            "link": "https://www.melintas.id/opini/346124379/kesehatan-mental-bukan-sekedar-trend-saatnya-serius-menata-dukungan-psikologis-di-indonesia",
            "image": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=400&h=200&q=80"
        },
        {
            "title": "Cara Mengelola Stres Akademik pada Mahasiswa",
            "description": "Tips dan strategi praktis untuk mengatasi tekanan akademik, mengatur waktu dengan baik, dan menjaga keseimbangan antara belajar dan kehidupan pribadi.",
            "link": "https://dit-mawa.upi.edu/tips-cara-mengatasi-stres-akademik/",
            "image": "https://cianjurkuy.id/wp-content/uploads/2024/03/388.jpg"
        },
        {
            "title": "Mengenali Gejala Depresi dan Kecemasan",
            "description": "Informasi tentang tanda-tanda awal depresi dan kecemasan, kapan harus mencari bantuan profesional.",
            "link": "https://ciputrahospital.com/depresi-dan-kecemasan-gangguan-kesehatan-mental-yang-perlu-kita-waspadai/",
            "image": "https://i0.wp.com/ciputrahospital.com/wp-content/uploads/2021/01/shutterstock_1347450608resizee.jpg?w=1024&ssl=1"
        },
        {
            "title": "Manfaat Meditasi untuk Kesehatan Mental",
            "description": "Meditasi bisa membantu kamu mendapatkan kembali fokus dan kesadaran diri.",
            "link": "https://www.halodoc.com/artikel/ketahui-5-manfaat-meditasi-untuk-kesehatan-mental?srsltid=AfmBOooUzcxHbVx1a1JgZ3ih4Gr2sXCgze7Eu0VWgC1NOIua6oxkeHr8",
            "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=400&h=200&q=80"
        },
        {
            "title": "Membangun Ketahanan Mental (Mental Resilience)",
            "description": "Cara membangun kemampuan untuk beradaptasi dengan menghadapi tantangan, memulihkan diri dari kesulitan, dan tumbuh lebih kuat dari pengalaman sulit.",
            "link": "https://positivepsychology.com/building-mental-resilience/",
            "image": "https://www.anahana.com/hs-fs/hubfs/Imported_Blog_Media/types-of-resilience-fourth-website-1.jpg?width=1300&height=650&name=types-of-resilience-fourth-website-1.jpg"
        },
        {
            "title": "Kesehatan Mental di Lingkungan Kampus",
            "description": "Panduan untuk menjaga kesehatan mental saat berada di lingkungan kampus yang penuh tekanan, termasuk cara membangun hubungan sosial yang sehat.",
            "link": "https://www.verywellmind.com/college-student-mental-health-4158297",
            "image": "https://pmb.unjani.ac.id/wp-content/uploads/2024/04/mental-health-care-sketch-diagram-1024x761.jpg"
        },
        {
            "title": "Ketika Harus Mencari Bantuan Profesional",
            "description": "Tanda-tanda kapan perlu mencari bantuan dari tenaga kesehatan mental profesional dan bagaimana cara mengakses layanan tersebut.",
            "link": "https://www.psychologytoday.com/us/basics/therapy",
            "image": "https://d1vbn70lmn1nqe.cloudfront.net/prod/wp-content/uploads/2024/04/01032358/Tips-Mencari-Psikiater-Terdekat-untuk-Penanganan-Gangguan-Kesehatan-Mental.jpg.webp"
        },
        {
            "title": "Gaya Hidup Sehat untuk Kesehatan Mental",
            "description": "Hubungan antara pola makan, olahraga, tidur, dan kesehatan mental, serta tips untuk menjaga keseimbangan antara semua aspek ini.",
            "link": "https://www.health.harvard.edu/mind-and-mood/regular-exercise-can-bolster-your-mental-health",
            "image": "https://tse1.mm.bing.net/th/id/OIP.wYqXrgfbJW6z1bwErNloUgHaEK?pid=Api&P=0&h=180"
        }
    ]

    for article in articles:
        st.image(article["image"], caption=article["title"], use_container_width=True)
        st.subheader(article["title"])
        st.write(article["description"])
        # Gunakan link button jika tersedia
        try:
            st.link_button("Baca Selengkapnya", article["link"])
        except AttributeError:
            st.markdown(f"[Baca Selengkapnya]({article['link']})", unsafe_allow_html=True)
        st.markdown("---")
