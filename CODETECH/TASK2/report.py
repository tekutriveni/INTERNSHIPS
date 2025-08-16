import pandas as pd
import matplotlib.pyplot as plt
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

# ---------- STEP 1: Sample Data ----------
data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Sales": [1200, 1500, 1700, 1600, 1800, 2100]
}
df = pd.DataFrame(data)

# ---------- STEP 2: Create a Chart ----------
plt.figure(figsize=(6, 4))
plt.plot(df["Month"], df["Sales"], marker='o', color='blue', linewidth=2)
plt.title("Monthly Sales Report")
plt.xlabel("Month")
plt.ylabel("Sales ($)")
plt.grid(True)

chart_path = "sales_chart.png"
plt.savefig(chart_path, bbox_inches='tight')
plt.close()

# ---------- STEP 3: Build PDF ----------
pdf_path = "Automated_Report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4)
styles = getSampleStyleSheet()
elements = []

# Add Title
elements.append(Paragraph("Automated Sales Report", styles['Title']))
elements.append(Spacer(1, 12))

# Add Summary Text
summary_text = f"""
This automated report shows monthly sales trends. 
The highest sales were recorded in {df.iloc[df['Sales'].idxmax()]['Month']} with ${df['Sales'].max()}.
The lowest sales were recorded in {df.iloc[df['Sales'].idxmin()]['Month']} with ${df['Sales'].min()}.
"""
elements.append(Paragraph(summary_text, styles['Normal']))
elements.append(Spacer(1, 12))

# Add Chart Image
elements.append(Image(chart_path, width=400, height=300))

# Save PDF
doc.build(elements)

# ---------- STEP 4: Open PDF Automatically ----------
print(f"✅ Report generated successfully: {pdf_path}")
os.startfile(pdf_path)  # Works on Windows
