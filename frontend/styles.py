"""Frontend styles and CSS for Panic2Pass."""

CUSTOM_CSS = """
/* Global Container Layout */
.gradio-container {
    max-width: 1240px !important;
    margin: 0 auto !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif !important;
}

/* Hero Header Banner */
.hero-header {
    text-align: center;
    padding: 24px 20px;
    margin-bottom: 18px;
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(249, 115, 22, 0.08) 50%, rgba(59, 130, 246, 0.06) 100%);
    border: 1px solid rgba(239, 68, 68, 0.22);
    border-radius: 18px;
    backdrop-filter: blur(12px);
}

.hero-title {
    font-size: 2.3rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
    margin-bottom: 4px !important;
    background: linear-gradient(90deg, #ef4444, #f97316, #eab308);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1.02rem !important;
    color: #64748b;
    font-weight: 500;
    margin-bottom: 10px !important;
}

/* Cache Status Pill */
.status-pill-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin-top: 8px;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px;
    border-radius: 9999px;
    font-size: 0.82rem;
    font-weight: 600;
    background: rgba(16, 185, 129, 0.12);
    color: #059669;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.dark .status-badge {
    background: rgba(16, 185, 129, 0.2);
    color: #34d399;
}

/* Action Buttons */
.btn-crash {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    border-radius: 12px !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.btn-crash:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.5) !important;
}

.btn-lost {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    border: none !important;
}

.btn-quiz {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    border: none !important;
}

.btn-cheat {
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    border: none !important;
}

/* Output Display Card */
.output-card {
    border-radius: 16px !important;
    padding: 20px !important;
    min-height: 500px !important;
    background: rgba(255, 255, 255, 0.75) !important;
    border: 1px solid rgba(226, 232, 240, 0.9) !important;
    backdrop-filter: blur(8px);
}

.dark .output-card {
    background: rgba(15, 23, 42, 0.75) !important;
    border: 1px solid rgba(51, 65, 85, 0.9) !important;
}
"""
