import streamlit as st
import streamlit.components.v1 as components
import time

def reload_on_back():
# Usamos un identificador único para esta carga de página
    timestamp = str(time.time())
    
    html_code = f"""
    <script>
    (function() {{
        const win = window.parent;
        
        // 1. Detectar navegación mediante el objeto performance (más robusto)
        const perfEntries = win.performance.getEntriesByType("navigation");
        if (perfEntries.length > 0 && perfEntries[0].type === "back_forward") {{
            win.location.reload();
        }}

        // 2. Escuchar el evento popstate del PADRE
        win.addEventListener('popstate', function(event) {{
            // Si el usuario le da a atrás, recargamos
            win.location.reload();
        }}, {{ once: true }});

        // 3. Empujar un estado al historial para que el botón "Atrás" tenga algo que activar
        if (!win.history.state || win.history.state.page_id !== "{timestamp}") {{
            win.history.pushState({{ page_id: "{timestamp}" }}, "");
        }}

        // --- Ocultar el componente para no dañar el diseño de EPI-SYSTEM ---
        const frames = win.document.querySelectorAll('iframe[title="st.iframe"]');
        frames.forEach(f => {{
            if (f.srcdoc.includes("back_forward")) {{
                const container = f.closest('div[data-testid="stHtml"]');
                if (container) {{
                    container.style.display = 'none';
                    container.style.position = 'absolute';
                }}
            }}
        }});
    }})();
    </script>
    """
    st.components.v1.html(html_code, height=0)

