import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# Fungsi untuk koneksi ke database Adventure Works
def create_connection():
    conn = st.connection(
        "mydb",
        type="sql", autocommit=True
    )
# Fungsi untuk menjalankan query
def run_query(query):
    conn = create_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
# Fungsi untuk memuat data IMDB dari CSV
def load_imdb():
    return pd.read_csv('imdb_top_scrapping.csv')

# Judul dashboard
st.title('Dashboard Visualisasi Data')

# Sidebar untuk memilih dataset dan jenis visualisasi
dataset = st.sidebar.selectbox('Pilih Dataset', ['Adventure Works', 'IMDB'])
visualization_type = st.sidebar.selectbox('Pilih Jenis Visualisasi', 
                                          ['Comparison', 'Composition', 'Distribution', 'Relationship'])

# Memuat dataset yang dipilih
if dataset == 'Adventure Works':
    st.header("Adventure Works")
    
    if visualization_type == 'Comparison':
        st.subheader("Comparison: Tren Penjualan Tahunan")
        query_comparison = """
        SELECT t.CalendarYear, SUM(fs.OrderQuantity) AS TotalOrderQuantity 
        FROM FactInternetSales fs 
        JOIN DimTime t ON fs.OrderDateKey = t.TimeKey 
        GROUP BY t.CalendarYear 
        ORDER BY t.CalendarYear;
        """
        df_comparison = run_query(query_comparison)
        fig = px.bar(df_comparison, x='CalendarYear', y='TotalOrderQuantity',
                     title='Tren Penjualan Tahunan',
                     labels={'CalendarYear': 'Tahun', 'TotalOrderQuantity': 'Total Order Quantity'},
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig)

        description = """
        Deskripsi Visualisasi:
        Grafik batang ini menampilkan total jumlah pesanan (Total Order Quantity) per tahun dari database Adventure Works untuk periode 2001 hingga 2004.
        """
        st.write(description)

        interpretation = """
        Interpretasi Data:

        **Tahun 2001**:
        - Pada tahun ini, total jumlah pesanan terlihat sangat rendah dibandingkan tahun-tahun berikutnya.
        - Hal ini bisa disebabkan karena berbagai faktor, seperti baru dimulainya operasi atau kurangnya pemasaran dan pengenalan produk di pasar.

        **Tahun 2002**:
        - Terjadi peningkatan jumlah pesanan, meskipun peningkatannya masih relatif kecil.
        - Peningkatan ini mungkin menunjukkan adanya upaya pemasaran yang mulai membuahkan hasil atau pengenalan produk yang lebih baik di pasar.

        **Tahun 2003**:
        - Peningkatan pesanan yang signifikan terlihat pada tahun ini. Total jumlah pesanan meningkat tajam dibandingkan dengan tahun 2002.
        - Lonjakan ini bisa mengindikasikan keberhasilan strategi pemasaran, peningkatan kualitas produk, atau pengenalan produk baru yang diterima dengan baik oleh pasar.

        **Tahun 2004**:
        - Total jumlah pesanan kembali meningkat signifikan, bahkan lebih tinggi dari tahun 2003.
        - Hal ini menunjukkan tren pertumbuhan yang sangat positif, yang bisa disebabkan oleh ekspansi pasar, peningkatan kepercayaan pelanggan, atau mungkin karena promosi dan diskon yang menarik bagi pelanggan.

        **Kesimpulan**:
        - Grafik ini menggambarkan tren penjualan yang sangat positif dan meningkat dari tahun ke tahun. Perusahaan tampaknya berhasil meningkatkan total jumlah pesanan setiap tahunnya, terutama setelah tahun 2002. Strategi pemasaran dan pengembangan produk yang baik kemungkinan besar memainkan peran penting dalam pencapaian ini. Melihat tren yang ada, perusahaan bisa terus mempertahankan dan meningkatkan strategi yang ada untuk menjaga pertumbuhan yang berkelanjutan di masa mendatang.
        """
        st.write(interpretation)

    elif visualization_type == 'Composition':
        st.subheader("Composition: Distribusi Penjualan Produk Berdasarkan Kategori")
        query_composition = """
        SELECT 
            dst.SalesTerritoryCountry AS TerritoryCountry, 
            SUM(fs.SalesAmount) AS TotalSalesAmount 
        FROM 
            DimSalesTerritory dst 
        JOIN 
            FactInternetSales fs ON dst.SalesTerritoryKey = fs.SalesTerritoryKey 
        GROUP BY 
            dst.SalesTerritoryCountry 
        ORDER BY 
            TotalSalesAmount DESC;
        """
        df_composition = run_query(query_composition)
        fig = px.pie(df_composition, values='TotalSalesAmount', names='TerritoryCountry',
                     title='Distribusi Penjualan Produk Berdasarkan Kategori',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig)

        description = """
        Deskripsi Visualisasi:
        Diagram pai ini menggambarkan persentase kontribusi penjualan dari berbagai wilayah penjualan (sales territory) dalam database Adventure Works. Wilayah-wilayah yang ditampilkan meliputi Amerika Serikat, Australia, Kanada, Prancis, Jerman, dan Inggris.
        """
        st.write(description)

        interpretation = """
        Interpretasi Data:

        **United States (32.0%)**:
        - Amerika Serikat merupakan wilayah dengan kontribusi penjualan terbesar, menyumbang 32% dari total penjualan.
        - Hal ini menunjukkan pasar yang sangat kuat di Amerika Serikat, yang mungkin disebabkan oleh basis pelanggan yang besar dan stabilitas ekonomi yang mendukung.

        **Australia (30.9%)**:
        - Australia adalah wilayah kedua terbesar dengan kontribusi sebesar 30.9%.
        - Ini menandakan bahwa produk Adventure Works sangat diterima di Australia, hampir setara dengan pasar Amerika Serikat.

        **United Kingdom (11.6%)**:
        - Inggris menyumbang 11.6% dari total penjualan.
        - Walaupun kontribusinya tidak sebesar Amerika Serikat atau Australia, Inggris tetap merupakan pasar yang signifikan.

        **Germany (9.9%)**:
        - Jerman memiliki kontribusi sebesar 9.9%.
        - Pasar ini juga penting, meskipun sedikit lebih kecil dibandingkan dengan Inggris.

        **France (9.0%)**:
        - Prancis menyumbang 9% dari total penjualan.
        - Sama seperti Jerman, Prancis merupakan pasar yang signifikan namun lebih kecil dari Inggris dan Jerman.

        **Canada (6.7%)**:
        - Kanada memiliki kontribusi terkecil di antara wilayah yang ditampilkan, dengan 6.7%.
        - Meskipun demikian, pasar Kanada masih memberikan kontribusi yang berarti bagi penjualan keseluruhan.

        **Kesimpulan**:
        - Diagram pai ini menunjukkan bahwa Amerika Serikat dan Australia adalah dua pasar terbesar bagi Adventure Works, mencakup lebih dari 60% dari total penjualan. Inggris, Jerman, Prancis, dan Kanada juga merupakan pasar penting, meskipun kontribusi mereka lebih kecil dibandingkan dengan Amerika Serikat dan Australia. Informasi ini bisa sangat berharga bagi perusahaan dalam menentukan strategi pemasaran dan distribusi di masa depan. Fokus dapat diarahkan pada mempertahankan dan meningkatkan penjualan di wilayah-wilayah utama, sambil mengeksplorasi peluang untuk meningkatkan kontribusi dari pasar yang lebih kecil.
        """
        st.write(interpretation)

    elif visualization_type == 'Distribution':
        st.subheader("Distribution: Distribusi Harga Produk")
        query_distribution = """
        SELECT FLOOR(p.ListPrice / 10) * 10 AS PriceRange, COUNT(*) AS Frequency 
        FROM DimProduct p 
        GROUP BY FLOOR(p.ListPrice / 10) * 10 
        ORDER BY PriceRange;
        """
        df_distribution = run_query(query_distribution)
        fig = px.scatter(df_distribution, x='PriceRange', y='Frequency',
                         title='Distribusi Harga Produk',
                         labels={'PriceRange': 'Rentang Harga', 'Frequency': 'Frekuensi'},
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig)

        description = """
        Deskripsi Visualisasi:
        Plot sebar (scatter plot) ini menampilkan distribusi harga produk dari database Adventure Works. Sumbu x menunjukkan rentang harga produk, sedangkan sumbu y menunjukkan frekuensi atau jumlah produk yang berada dalam rentang harga tertentu.
        """
        st.write(description)

        interpretation = """
        Interpretasi Data:

        **Rentang Harga 0 - 500**:
        - Terlihat beberapa produk dalam rentang harga ini dengan frekuensi yang cukup tersebar. Rentang ini mencakup produk-produk dengan harga yang lebih rendah.
        - Frekuensi produk di rentang harga ini bervariasi, dengan beberapa titik yang menunjukkan adanya beberapa produk yang harganya berada dalam kisaran ini.

        **Rentang Harga 500 - 1000**:
        - Rentang harga ini menunjukkan frekuensi yang lebih tinggi, dengan beberapa titik yang memiliki frekuensi lebih dari 10.
        - Ini menandakan bahwa banyak produk berada dalam kisaran harga ini, menunjukkan popularitas atau volume produk yang lebih tinggi pada harga ini.

        **Rentang Harga 1000 - 2000**:
        - Frekuensi produk dalam rentang ini mulai menurun. Titik-titik di grafik menunjukkan distribusi produk yang lebih sedikit dibandingkan rentang harga sebelumnya.
        - Menandakan bahwa produk dalam kisaran harga ini kurang umum dibandingkan produk yang lebih murah.

        **Rentang Harga 2000 - 3000**:
        - Hanya sedikit produk yang berada dalam kisaran harga ini, dengan frekuensi yang lebih rendah.
        - Produk dalam kisaran harga ini mungkin merupakan produk-produk premium atau spesifik yang ditawarkan oleh Adventure Works.

        **Rentang Harga di atas 3000**:
        - Frekuensi produk dalam rentang harga ini sangat rendah, menunjukkan hanya beberapa produk yang memiliki harga tinggi.
        - Produk-produk dalam kategori ini kemungkinan adalah produk premium atau dengan fitur khusus yang membedakannya dari produk lain.

        **Kesimpulan**:
        Plot sebar ini menunjukkan bahwa mayoritas produk Adventure Works berada dalam rentang harga 0 hingga 1000, dengan konsentrasi tertinggi di kisaran 500 hingga 1000. Jumlah produk menurun secara signifikan pada rentang harga yang lebih tinggi, menunjukkan bahwa produk premium atau mahal lebih jarang. Informasi ini dapat membantu perusahaan dalam strategi penetapan harga dan pengembangan produk. Fokus dapat diarahkan pada penguatan pasar untuk produk dalam rentang harga menengah, sekaligus mengeksplorasi peluang untuk memperkenalkan produk baru di segmen premium.
        """
        st.write(interpretation)

    elif visualization_type == 'Relationship':
        st.subheader("Relationship: Hubungan antara Harga Produk dengan Jumlah Transaksi")
        query_relationship = """
        SELECT p.ListPrice, COUNT(*) AS TransactionCount 
        FROM FactInternetSales fs 
        JOIN DimProduct p ON fs.ProductKey = p.ProductKey 
        GROUP BY p.ListPrice 
        ORDER BY p.ListPrice;
        """
        df_relationship = run_query(query_relationship)
        fig = px.scatter(df_relationship, x='ListPrice', y='TransactionCount',
                         title='Hubungan antara Harga Produk dengan Jumlah Transaksi',
                         labels={'ListPrice': 'Harga Produk', 'TransactionCount': 'Jumlah Transaksi'},
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig)

        description = """
        Deskripsi Visualisasi:
        Diagram scatter ini menunjukkan hubungan antara harga produk dan jumlah transaksi dalam database Adventure Works.
        Setiap titik merepresentasikan harga produk tertentu dan jumlah transaksi yang terkait dengan harga tersebut.
        """
        st.write(description)

        interpretation = """
        Interpretasi Data:
        **Distribusi Data**:
- Sebagian besar produk memiliki harga di bawah 500.
- Jumlah transaksi menurun seiring dengan kenaikan harga produk.

        **Korelasi Negatif**:
- Terdapat korelasi negatif antara harga produk dan jumlah transaksi. Artinya, produk dengan harga lebih rendah cenderung memiliki jumlah transaksi yang lebih tinggi.
- Produk dengan harga sangat tinggi (>2000) memiliki jumlah transaksi yang relatif rendah. Ini menunjukkan bahwa produk mahal mungkin memiliki pasar yang lebih terbatas.
        **Outlier**:
- Terdapat beberapa outlier yang mencolok, di mana produk dengan harga di bawah 500 tetapi jumlah transaksinya sangat tinggi (lebih dari 6000). Ini mungkin menunjukkan produk yang sangat populer atau diskon besar-besaran.
         """
        st.write(interpretation)

elif dataset == 'IMDB':
    st.header("IMDB")
    df = load_imdb()
    
    st.markdown("---")  # Pembatas

    if visualization_type == 'Comparison':
        st.subheader("Comparison: Perbandingan Jumlah Film berdasarkan Negara Asal (Top 10)")
        country_counts = df['Country of Origin'].value_counts().head(10)
        fig = px.bar(country_counts, x=country_counts.index, y=country_counts.values,
                     title='Perbandingan Jumlah Film berdasarkan Negara Asal (Top 10)',
                     labels={'x': 'Negara Asal', 'y': 'Jumlah Film'},
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig)

        description = """
        Visualisasi: Perbandingan Jumlah Film berdasarkan Negara Asal
Deskripsi Visualisasi
Visualisasi ini menunjukkan perbandingan jumlah film berdasarkan negara asal dalam bentuk bar chart. Visualisasi ini membandingkan jumlah film dari negara-negara yang termasuk dalam sepuluh besar.

Interpretasi Data
Dominasi Amerika Serikat:

Amerika Serikat menempati posisi teratas dengan jumlah film terbanyak, yaitu sekitar 20 film. Hal ini menunjukkan dominasi Amerika Serikat dalam industri film global, kemungkinan besar karena Hollywood yang merupakan pusat industri film terbesar di dunia.
Negara Lain dengan Jumlah Film Signifikan:

Selanjutnya adalah Selandia Baru, Jerman, Jepang, dan Brasil, meskipun jumlah film dari negara-negara ini jauh lebih rendah dibandingkan dengan Amerika Serikat.
Selandia Baru berada di posisi kedua, menunjukkan kontribusi signifikan dalam industri film, meskipun jumlah filmnya tidak sebanyak Amerika Serikat.
Distribusi yang Tidak Merata:

Ada kesenjangan yang cukup besar antara jumlah film dari Amerika Serikat dan negara-negara lainnya. Negara-negara di luar Amerika Serikat memiliki jumlah film yang relatif lebih sedikit, yang menunjukkan konsentrasi produksi film di beberapa negara utama..
        """
        st.write(description)

    elif visualization_type == 'Composition':
        st.subheader("Composition: Proporsi Genre Film Teratas")
        genre_counts = df['Genre'].value_counts()
        fig = px.pie(genre_counts, values=genre_counts, names=genre_counts.index,
                     title='Proporsi Genre Film Teratas',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig)

        description = """
        Deskripsi Visualisasi:
        Visualisasi di atas menunjukkan proporsi genre film teratas yang diambil dari dataset IMDB dalam bentuk diagram pie (kue). Setiap bagian dari diagram pie merepresentasikan satu genre dengan persentase yang menunjukkan seberapa besar proporsi genre tersebut dibandingkan dengan genre lainnya.

Analisis dan Interpretasi
Action (36%):
Genre action mendominasi dengan proporsi terbesar yaitu 36%. Hal ini menunjukkan bahwa film action sangat populer di kalangan penonton, mungkin karena adegan yang penuh aksi, efek visual yang menakjubkan, dan alur cerita yang menegangkan.

Crime (28%):
Film dengan genre crime berada di urutan kedua dengan proporsi 28%. Popularitas genre ini dapat disebabkan oleh minat penonton terhadap cerita-cerita yang berhubungan dengan kejahatan, investigasi, dan misteri yang sering kali menantang pikiran.

Drama (24%):
Drama menempati posisi ketiga dengan proporsi 24%. Genre ini cenderung menarik perhatian penonton yang menyukai cerita-cerita yang menyentuh emosi, pengembangan karakter yang mendalam, dan konflik-konflik personal yang kompleks.

Biography (8%):
Genre biografi memiliki proporsi 8%. Meskipun proporsinya lebih kecil dibandingkan dengan genre lainnya, film biografi sering kali memberikan wawasan menarik tentang kehidupan tokoh-tokoh nyata dan peristiwa bersejarah.

Adventure (4%):
Genre petualangan (adventure) memiliki proporsi terkecil dengan 4%. Meskipun demikian, film petualangan tetap memiliki daya tarik tersendiri, terutama bagi penonton yang menikmati eksplorasi, perjalanan, dan kisah-kisah epik.

Kesimpulan
Dari visualisasi ini, kita dapat melihat bahwa film action, crime, dan drama adalah tiga genre teratas yang paling banyak diproduksi dan disukai oleh penonton berdasarkan dataset IMDB. Sementara itu, genre biografi dan petualangan memiliki proporsi yang lebih kecil namun tetap signifikan. Pemahaman ini dapat membantu para pembuat film, peneliti, dan penggemar film untuk mengenali tren dan preferensi di industri film.
        """
        st.write(description)

    elif visualization_type == 'Distribution':
        st.subheader("Distribution: Distribusi Rating IMDb Berdasarkan Genre")
        fig = px.box(df, x='Genre', y='Film Rating',
                     title='Distribusi Rating IMDb Berdasarkan Genre',
                     labels={'Genre': 'Genre', 'Film Rating': 'Rating IMDb'},
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig)

        description = """
        Deskripsi Visualisasi:
        Visualisasi ini memperlihatkan distribusi rating IMDb untuk berbagai genre film dalam bentuk box plot. Box plot ini membantu kita memahami bagaimana rating tersebar untuk masing-masing genre, termasuk nilai median, rentang antar kuartil, serta kemungkinan adanya outlier.

Analisis dan Interpretasi
Drama:

Rentang rating: sekitar 8.8 hingga 9.2
Median: sekitar 9.0
Drama memiliki distribusi rating yang tinggi dan konsisten dengan rentang yang sempit, menunjukkan bahwa film-film drama cenderung mendapatkan rating yang stabil dan tinggi dari penonton.
Crime:

Rentang rating: sekitar 8.8 hingga 9.1
Median: sekitar 9.0
Genre crime juga memiliki rating yang relatif tinggi dengan rentang yang sedikit lebih luas dibandingkan dengan drama, menandakan adanya variasi dalam penilaian penonton terhadap film-film crime.
Action:

Rentang rating: sekitar 8.5 hingga 8.9
Median: sekitar 8.7
Film action menunjukkan distribusi rating yang lebih luas dengan beberapa outlier, mengindikasikan variasi yang lebih besar dalam penilaian penonton. Beberapa film mungkin sangat populer, sementara yang lain mungkin kurang diterima.
Biography:

Rentang rating: sekitar 8.6 hingga 8.9
Median: sekitar 8.75
Film biografi memiliki rentang rating yang sempit dan konsisten, menunjukkan bahwa genre ini umumnya diterima dengan baik oleh penonton dengan sedikit variasi dalam penilaian.
Adventure:

Rentang rating: sekitar 8.5 hingga 8.6
Median: sekitar 8.55
Genre adventure menunjukkan rentang rating yang sangat sempit dengan nilai median yang lebih rendah dibandingkan genre lain, menandakan penilaian yang lebih seragam tetapi cenderung lebih rendah.
Kesimpulan
Dari visualisasi ini, kita dapat menyimpulkan bahwa film-film dalam genre drama dan crime umumnya mendapatkan rating yang tinggi dan stabil dari penonton IMDb, sementara genre action menunjukkan variasi yang lebih besar dalam rating. Film biografi cenderung memiliki penilaian yang konsisten dan baik, sedangkan film adventure meskipun dinilai secara seragam, memiliki rating yang lebih rendah dibandingkan genre lainnya.
        """
        st.write(description)

    elif visualization_type == 'Relationship':
        st.subheader("Relationship: Relationship antara Gross Worldwide dan Opening Weekend US and Canada")
        fig = px.scatter(df, x='Gross Worldwide', y='Opening Weekend US and Canada',
                         title='Relationship antara Gross Worldwide dan Opening Weekend US and Canada',
                         labels={'Gross Worldwide': 'Gross Worldwide (dalam miliar $)', 'Opening Weekend US and Canada': 'Opening Weekend US and Canada (dalam juta $)'},
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(marker=dict(size=12))
        fig.update_layout(xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
        st.plotly_chart(fig)

        description = """
        Deskripsi Visualisasi:
        Visualisasi ini menggunakan diagram scatter untuk menunjukkan hubungan antara pendapatan kotor global (Gross Worldwide) dan pendapatan akhir pekan pembukaan (Opening Weekend) di AS dan Kanada. Setiap titik dalam diagram mewakili sebuah film.

Analisis dan Interpretasi
Korelasi Positif:

Secara umum, terdapat korelasi positif antara pendapatan akhir pekan pembukaan di AS dan Kanada dengan pendapatan kotor global. Artinya, semakin tinggi pendapatan yang diperoleh pada akhir pekan pembukaan, semakin tinggi pula pendapatan kotor global yang dihasilkan film tersebut.
Pendapatan Akhir Pekan Pembukaan Tinggi:

Film dengan pendapatan akhir pekan pembukaan yang sangat tinggi (di atas $100 juta) cenderung memiliki pendapatan kotor global yang juga tinggi (mencapai miliaran dolar). Hal ini menunjukkan bahwa performa awal di pasar domestik bisa menjadi indikator kuat untuk kesuksesan global.
Variasi di Pendapatan Akhir Pekan Pembukaan Rendah:

Film dengan pendapatan akhir pekan pembukaan yang lebih rendah menunjukkan variasi yang lebih besar dalam pendapatan kotor global. Beberapa film dengan pendapatan pembukaan yang rendah tetap berhasil meraih pendapatan global yang cukup tinggi, mungkin karena faktor-faktor seperti ulasan positif, promosi mulut ke mulut, atau kekuatan pasar internasional.
Distribusi Titik:

Titik-titik data terdistribusi secara berkelompok pada pendapatan akhir pekan pembukaan yang lebih rendah, dengan beberapa outlier di pendapatan tinggi. Ini menunjukkan bahwa banyak film memiliki pendapatan pembukaan yang lebih sederhana namun ada beberapa blockbuster yang mencetak pendapatan besar baik di pembukaan akhir pekan maupun secara global.
Kesimpulan
Visualisasi ini mengungkapkan bahwa terdapat hubungan yang kuat antara pendapatan pembukaan akhir pekan di AS dan Kanada dengan pendapatan kotor global. Pendapatan pembukaan yang tinggi sering kali menjadi indikasi awal kesuksesan global, sementara film-film dengan pembukaan yang lebih rendah memiliki hasil yang lebih bervariasi di pasar global. Informasi ini penting bagi para produser film, distributor, dan pemasar dalam merencanakan strategi rilis dan promosi film.
        """
        st.write(description)
