import streamlit as st
import streamlit.components.v1 as components

def reload_on_back():
    html_code = """
    <script>
    (function() {
        window.addEventListener('pageshow', function(event) {
            // event.persisted es true si la página se cargó desde el bfcache (retroceder/adelantar)
            // window.performance.navigation.type === 2 es la forma antigua para navegadores viejos
            if (event.persisted || (window.performance && window.performance.navigation.type === 2)) {
                window.location.reload();
            }
        });
        
        // Ocultar el componente para que no desajuste el login
        const doc = window.parent.document;
        const frames = doc.querySelectorAll('iframe[title="st.iframe"]');
        frames.forEach(f => {
            if (f.srcdoc.includes("pageshow")) {
                f.parentElement.style.display = 'none';
                f.parentElement.style.position = 'absolute';
            }
        });
    })();
    </script>
    """
    st.components.v1.html(html_code, height=0)

