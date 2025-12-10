import matplotlib.pyplot as plt
import matplotlib.cm as cm # Renk paleti için

# --- 1. VERİ GİRİŞİ ---
data = {
    'A': [17.49, 8.22, 3.82, 0.85],
    'B': [15.66, 3.89, 4.28, 2.26],
    'C': [17.45, 6.59, 4.32, 1.42],
    'D': [15.75, 4.59, 3.89, 2.11],
    'E': [20.12, 10.05, 3.46, 0.68],
    'F': [15.34, 3.85, 4.11, 1.18],
    'G': [15.23, 4.59, 3.89, 1.43],
    'H': [15.50, 4.36, 3.32, 1.38],
    'I': [16.17, 4.24, 4.08, 1.12],
    'J': [15.23, 4.74, 4.46, 0.98],
    'K': [15.73, 5.74, 2.95, 0.87],
    'L': [15.66, 6.00, 5.67, 0.49],
    'M': [16.76, 6.64, 5.13, 0.62]
}

# Molekül Ağırlıkları
mw = {'Al2O3': 101.96, 'CaO': 56.077, 'Na2O': 61.97, 'K2O': 94.2}

# --- 2. HESAPLAMA MOTORU ---
points = {}
cia_values = {}
comp_values = {} # Sonuçları yazdırmak için bileşenleri saklayacağız

for sample, oxides in data.items():
    # Ağırlıkça % -> Mol Dönüşümü
    m_al = oxides[0] / mw['Al2O3']
    m_ca = oxides[1] / mw['CaO']
    m_na = oxides[2] / mw['Na2O']
    m_k  = oxides[3] / mw['K2O']
    
    # CIA Hesaplama
    cia = (m_al / (m_al + m_ca + m_na + m_k)) * 100
    cia_values[sample] = cia
    
    # Üçgen Koordinatları (A - CN - K)
    sum_components = m_al + (m_ca + m_na) + m_k
    
    a_pct = (m_al / sum_components) * 100
    cn_pct = ((m_ca + m_na) / sum_components) * 100
    k_pct = (m_k / sum_components) * 100
    
    # İleride yazdırmak için saklayalım
    comp_values[sample] = (a_pct, cn_pct, k_pct)
    
    # Kartezyen Dönüşüm (X, Y)
    # Sol Alt (CN)=0,0 | Sağ Alt (K)=100,0 | Tepe (A)=50, 86.6
    x = k_pct + (a_pct * 0.5)
    y = a_pct * (np.sqrt(3) / 2)
    
    points[sample] = (x, y)

# --- 3. ÇİZİM (MATPLOTLIB) ---
fig, ax = plt.subplots(figsize=(12, 10)) # Lejant için alanı biraz genişlettik

# Üçgen Çerçevesi
triangle_x = [0, 100, 50, 0]
triangle_y = [0, 0, 50 * np.sqrt(3), 0]
ax.plot(triangle_x, triangle_y, 'k-', lw=1.5)

# Köşe Etiketleri 
ax.text(50, 90, 'Al$_2$O$_3$ (A)\nKaolinite/Gibbsite', ha='center', fontsize=12, fontweight='bold')
ax.text(-5, -5, 'CaO + Na$_2$O (CN)', ha='right', fontsize=12, fontweight='bold')
ax.text(105, -5, 'K$_2$O (K)', ha='left', fontsize=12, fontweight='bold')

# Feldspar Çizgisi (%50 Al - Teorik)
# A noktası (Tepe) ile CN-K hattının ortası arasındaki %50 çizgisi
ax.plot([25, 75], [43.3, 43.3], 'k--', lw=0.8, alpha=0.5, label='Feldspar Hattı (%50)')

# --- NUMUNELERİ RENKLENDİRME ---
# Numune sayısı kadar renk üret (tab20 paleti kullanıldı, canlı ve ayrık renkler verir)
colors = cm.tab20(np.linspace(0, 1, len(data)))

for i, (sample, (x, y)) in enumerate(points.items()):
    # Her numune için o numuneye özel renk seç
    c = colors[i]
    
    ax.plot(x, y, marker='o', markersize=9, color=c, markeredgecolor='k', alpha=0.9, label=sample)
    # Numune adını noktanın hemen yanına yaz
    ax.text(x + 1.5, y, sample, fontsize=9, fontweight='bold', color=c)

# CIA Ölçeğini Yan Tarafa Ekleme
ax.plot([-10, -10], [0, 50*np.sqrt(3)], 'k-', lw=1)
for i in range(0, 110, 10):
    h = i * (50*np.sqrt(3) / 100)
    ax.plot([-12, -10], [h, h], 'k-')
    ax.text(-15, h, str(i), ha='right', va='center', fontsize=8)
ax.text(-20, 43, 'CIA Scale', ha='center', fontsize=12, rotation=90)

# Ayarlar
ax.set_aspect('equal')
ax.axis('off')
plt.title('CIA Ternary Diagram (A-CN-K)', fontsize=16, y=1.05)

# İsterseniz dışarıda bir lejant (legend) da gösterebilirsiniz:
# plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))

plt.show()

# --- KONSOL ÇIKTISI ---
print(f"{'Sample':<6} | {'CIA':<6} | {'A %':<6} | {'CN %':<6} | {'K %':<6}")
print("-" * 46)
for s in data.keys():
    a, cn, k = comp_values[s]
    print(f"{s:<6} | {cia_values[s]:<6.1f} | {a:<6.1f} | {cn:<6.1f} | {k:<6.1f}")