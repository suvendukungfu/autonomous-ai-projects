from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_sample_contract():
    c = canvas.Canvas("sample_risky_contract.pdf", pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "MASTER SERVICES AGREEMENT - SAMPLE")

    # Introduction
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, "This Agreement is made as of 2026-02-24 by and between Client and Vendor.")

    # 1. Indemnity Clause (High Risk)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 130, "1. Indemnification")
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 150, "Vendor agrees to unconditionally indemnify and hold Client harmless from any")
    c.drawString(50, height - 165, "and all claims, damages, indirect losses, or punitive liabilities whatsoever")
    c.drawString(50, height - 180, "arising out of this Agreement, regardless of fault or negligence.")

    # 2. Payment Terms (Medium Risk)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 220, "2. Payment and Penalties")
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 240, "Client shall pay undisputed invoices within 90 days of receipt.")
    c.drawString(50, height - 255, "If Client disputes any portion, Vendor may not suspend services.")
    c.drawString(50, height - 270, "Vendor is liable for a penalty of $500 per day for any minor delays.")

    # 3. Termination Clause (High Risk)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 310, "3. Termination")
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 330, "Client may terminate this Agreement at any time, for any reason, without notice.")
    c.drawString(50, height - 345, "Upon such termination, Vendor shall forfeit all unpaid fees for work completed.")
    c.drawString(50, height - 360, "Vendor has no right to terminate this Agreement under any circumstances.")

    # 4. Liability Limitation (Low/Medium Risk)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 400, "4. Limitation of Liability")
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 420, "Client's total aggregate liability under this agreement shall not exceed $10.")
    c.drawString(50, height - 435, "Vendor's liability remains completely uncapped.")

    c.save()
    print("Generated sample_risky_contract.pdf successfully.")

if __name__ == "__main__":
    create_sample_contract()
