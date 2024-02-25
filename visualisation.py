import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap


df = pd.read_csv('../taxi.csv')

# --------------------------------------------
# Średni czas podróży

avg_travel_time = df['trip_seconds'].mean()

plt.figure()
plt.bar('Średni czas podróży w minutach', avg_travel_time/60)
plt.ylabel('Minuty')
plt.title(f'Średni czas podróży: {avg_travel_time/60}')


# --------------------------------------------
# Średnia odległość przejazdu

avg_travel_miles = df['trip_miles'].mean()
plt.figure()
plt.bar('Średnia odległość przejazdu', avg_travel_miles)
plt.ylabel('Mile')
plt.title(f'Średnia odległość przejazdu: {avg_travel_miles}')

# --------------------------------------------
# Minimalny i maksymalny czas oraz odległość (bez zerowych wartości)

df_filtered = df[(df['trip_seconds'] > 0) & (df['trip_miles'] > 0)]
min_travel_time = df_filtered['trip_seconds'].min()
min_distance = df_filtered['trip_miles'].min()
max_travel_time = df['trip_seconds'].max()
max_distance = df['trip_miles'].max()

parameters = [f'Minimalny czas podróży: {min_travel_time}', f'Maksymalny czas podróży: {max_travel_time}', f'Minimalna odległość: {min_distance}', f'Maksymalna odległość: {max_distance}']

values = [min_travel_time, max_travel_time, min_distance, max_distance]

plt.figure()
plt.bar(parameters, values, color=['skyblue', 'salmon', 'lightgreen', 'gold'])
plt.ylabel('Znaczenie')
plt.title('Minimalny i maksymalny czas oraz odległość (bez zerowych wartości)')
plt.xticks(rotation=45)


# --------------------------------------------
# Srednia i mediana opłaty za podróż

df_filtered = df['trip_total'] > 0
avg_price = df['trip_total'].mean()
median_price = df['trip_total'].median()

plt.figure()
plt.plot([f'Średnia opłata: {avg_price}', f'Mediana opłata: {median_price}'], [avg_price, median_price], marker='o', color='skyblue')
plt.xlabel('Parametr')
plt.ylabel('Cena')
plt.title('Średnie i medianowe wartości opłaty za podróż')
plt.grid(True)


# --------------------------------------------
# Liczba wystąpień dla każdej strefy posadzenia

pickup_counts = df['pickup_community_area'].value_counts().head(10)  # 10 najczęściej występujących stref
dropoff_counts = df['dropoff_community_area'].value_counts().head(10)  # 10 najczęściej występujących stref
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
pickup_counts.plot(kind='bar', color='skyblue')
plt.title('Najpopularniejsze strefy posadzenia')
plt.xlabel('Strefa posadzenia')
plt.ylabel('Liczba wystąpień')

plt.subplot(1, 2, 2)
dropoff_counts.plot(kind='bar', color='salmon')
plt.title('Najpopularniejsze strefy wysadzenia')
plt.xlabel('Strefa wysadzenia')
plt.ylabel('Liczba wystąpień')

plt.tight_layout()

# --------------------------------------------
podroze_w_gminach = df['pickup_community_area'].value_counts()

plt.figure(figsize=(10, 6))
plt.bar(podroze_w_gminach.index, podroze_w_gminach.values, color='skyblue')
plt.xlabel('Community area')
plt.ylabel('Liczba podróży')
plt.title('Czestliwosc podróży w Community areas')
plt.xticks(rotation=90)


# --------------------------------------------
# HeatMap dla poczatku przejazdu

df_cleaned = df.dropna(subset=['pickup_latitude', 'pickup_longitude'])

mapa = folium.Map(location=[41.8781, -87.6298], zoom_start=11)  # Ustawiam początkowe współrzędne i przybliżenie mapy

punkty_poczatkowe = df_cleaned[['pickup_latitude', 'pickup_longitude']].values.tolist()

HeatMap(punkty_poczatkowe).add_to(mapa)

mapa

# --------------------------------------------
# HeatMap dla zakonczenia przejazdu

df_cleaned = df.dropna(subset=['dropoff_latitude', 'dropoff_longitude'])

mapa = folium.Map(location=[41.8781, -87.6298], zoom_start=11)  # Ustawiam początkowe współrzędne i przybliżenie mapy

punkty_poczatkowe = df_cleaned[['dropoff_latitude', 'dropoff_longitude']].values.tolist()

HeatMap(punkty_poczatkowe).add_to(mapa)

mapa

# --------------------------------------------
# Oblicz sumę dodatkowych kosztów (tolls, extras)

sum_of_add_spendings = df[['tolls', 'extras']].sum().sum()

plt.figure(figsize=(8, 6))
plt.pie(df[['tolls', 'extras']].sum(), labels=['Tolls', 'Extras'], autopct='%1.1f%%', colors=['skyblue', 'salmon'], startangle=140)
plt.title('Analiza dodatkowych kosztów (tolls, extras)')
plt.axis('equal')


# --------------------------------------------
#Średni procent napiwków według typu płatności

df['tip_percent'] = (df['tips'] / df['trip_total']) * 100

tip_percent_by_payment_type = df.groupby('payment_type')['tip_percent'].mean()

plt.figure(figsize=(10, 6))
tip_percent_by_payment_type.plot(kind='bar', color='skyblue')
plt.xlabel('Typ płatności')
plt.ylabel('Średni procent napiwków')
plt.title('Średni procent napiwków według typu płatności')
plt.xticks(rotation=45)


# --------------------------------------------
#Przydzial dlugosci przejadu

plt.figure(figsize=(10, 6))
plt.scatter(df['trip_seconds'], df['trip_seconds'].groupby(df['trip_seconds']).transform('count'), color='skyblue', alpha=0.5)
plt.title('Przydzial dlugosci przejadu')
plt.xlabel('Dlugosc przejazdu (sek)')
plt.ylabel('Czestotliwosc')
plt.ylim(0, 10000)

# --------------------------------------------
#Analiza aktywności w ciągu dnia

df['trip_start_timestamp'] = pd.to_datetime(df['trip_start_timestamp'])

df['hour'] = df['trip_start_timestamp'].dt.hour

plt.figure(figsize=(10, 6))
plt.hist(df['hour'], bins=24, color='skyblue', edgecolor='black')
plt.xlabel('Godzina dnia')
plt.ylabel('Liczba podróży')
plt.title('Analiza aktywności w ciągu dnia')
plt.xticks(range(24))
plt.grid(axis='y', linestyle='--', alpha=0.7)

# --------------------------------------------
#Analiza aktywności w ciągu tygodnia

df['trip_start_timestamp'] = pd.to_datetime(df['trip_start_timestamp'])

df['day_of_week'] = df['trip_start_timestamp'].dt.dayofweek

plt.figure(figsize=(10, 6))
df['day_of_week'].value_counts().sort_index().plot(kind='bar', color='skyblue', edgecolor='black')
plt.xlabel('Dzień tygodnia')
plt.ylabel('Liczba podróży')
plt.title('Analiza aktywności w ciągu tygodnia')
plt.xticks(range(7), ['Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sob', 'Ndz'], rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)


# --------------------------------------------
#Analiza aktywności w ciągu roku

df['trip_start_timestamp'] = pd.to_datetime(df['trip_start_timestamp'])

df['month'] = df['trip_start_timestamp'].dt.month

monthly_trip_counts = df['month'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
monthly_trip_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.xlabel('Miesiąc')
plt.ylabel('Liczba podróży')
plt.title('Zmiana liczby podróży w różnych miesiącach')
plt.xticks(range(1, 13), ['Sty', 'Lut', 'Mar', 'Kwi', 'Maj', 'Cze', 'Lip', 'Sie', 'Wrz', 'Paź', 'Lis', 'Gru'], rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)


# --------------------------------------------
# Średni czas podróży w różnych porach dnia

df['trip_start_timestamp'] = pd.to_datetime(df['trip_start_timestamp'])

df['hour'] = df['trip_start_timestamp'].dt.hour

average_trip_duration_by_hour = df.groupby('hour')['trip_seconds'].mean() / 60

plt.figure(figsize=(10, 6))
plt.plot(average_trip_duration_by_hour.index, average_trip_duration_by_hour.values, marker='o', color='skyblue')
plt.xlabel('Godzina dnia')
plt.ylabel('Średni czas podróży (minuty)')
plt.title('Średni czas podróży w różnych porach dnia')
plt.xticks(range(24))
plt.grid(True, linestyle='--', alpha=0.7)


# --------------------------------------------
# Rozkład sposobów płatności

payment_counts = df['payment_type'].value_counts()
plt.figure(figsize=(8, 6))
payment_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.xlabel('Sposób płatności')
plt.ylabel('Liczba wystąpień')
plt.title('Rozkład sposobów płatności')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)


# --------------------------------------------
# Średnia wartość płatności w zależności od typu płatności

mean_payment_by_type = df.groupby('payment_type')['trip_total'].mean()

plt.figure(figsize=(8, 6))
mean_payment_by_type.plot(kind='bar', color='skyblue', edgecolor='black')
plt.xlabel('Typ płatności')
plt.ylabel('Średnia wartość płatności')
plt.title('Średnia wartość płatności w zależności od typu płatności')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)


# --------------------------------------------
# Trendy w używaniu różnych sposobów płatności w czasie

df['trip_start_timestamp'] = pd.to_datetime(df['trip_start_timestamp'])

df['year_month'] = df['trip_start_timestamp'].dt.to_period('M')

payment_trend = df.groupby(['year_month', 'payment_type']).size().unstack(fill_value=0)

plt.figure(figsize=(10, 6))
payment_trend.plot(kind='line', marker='o', linewidth=2)
plt.xlabel('Rok-Miesiąc')
plt.ylabel('Liczba transakcji')
plt.title('Trendy w używaniu różnych sposobów płatności w czasie')
plt.xticks(rotation=45)
plt.legend(title='Typ płatności', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()


# --------------------------------------------
# Popularność firm taksówkowych

company_counts = df['company'].value_counts()

plt.figure(figsize=(10, 6))
company_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.xlabel('Firma taksówkowa')
plt.ylabel('Liczba wystąpień')
plt.title('Popularność firm taksówkowych')
plt.xticks(rotation=90)
plt.grid(axis='y', linestyle='--', alpha=0.7)


# --------------------------------------------
# Średnia wartość płatności w zależności od firmy taksówkowej

average_payment_by_company = df.groupby('company')['trip_total'].mean()

plt.figure(figsize=(10, 6))
plt.scatter(average_payment_by_company.index, average_payment_by_company.values, color='skyblue')
plt.xlabel('Firma taksówkowa')
plt.ylabel('Średnia wartość płatności')
plt.title('Średnia wartość płatności w zależności od firmy taksówkowej')
plt.xticks(rotation=90)
plt.grid(True, linestyle='--', alpha=0.7)


# --------------------------------------------
# Porównanie srednich cen różnych firmach taksówkowych

average_payment_by_company = df.groupby('company')['trip_total'].mean()

average_trip_miles_by_company = df.groupby('company')['trip_miles'].mean()
companies = average_payment_by_company.index
plt.figure(figsize=(10, 6))
plt.scatter(average_trip_miles_by_company, average_payment_by_company, color='skyblue')
plt.xlabel('Średnia dlugosc przejazdu')
plt.ylabel('Średnia wartość płatności')
plt.title('Porównanie srednich cen różnych firmach taksówkowych')

for company, x, y in zip(companies, average_trip_miles_by_company, average_payment_by_company):
    plt.text(x, y, company, fontsize=8, ha='right', va='bottom')

plt.grid(True, linestyle='--', alpha=0.7)


# --------------------------------------------
# Korelacja między długością podróży a opłatą

df_clean = df.dropna(subset=['trip_seconds', 'trip_total'])

plt.figure(figsize=(10, 6))
plt.scatter(df_clean['trip_seconds'] / 60, df_clean['trip_total'], color='skyblue')
plt.xlabel('Długość podróży (minuty)')
plt.ylabel('Opłata')
plt.title('Korelacja między długością podróży a opłatą')

correlation = np.corrcoef(df_clean['trip_seconds'] / 60, df_clean['trip_total'])[0, 1]
plt.text(0.1, 0.9, f'Współczynnik korelacji: {correlation:.2f}', fontsize=10, transform=plt.gca().transAxes)

plt.grid(True, linestyle='--', alpha=0.7)

# --------------------------------------------
# Wpływ czasu dnia na rozmiar opłaty

df['trip_start_timestamp'] = pd.to_datetime(df['trip_start_timestamp'])
df['hour_of_day'] = df['trip_start_timestamp'].dt.hour
plt.figure(figsize=(10, 6))
plt.scatter(df['hour_of_day'], df['trip_total'], color='skyblue', alpha=0.5)
plt.xlabel('Godzina dnia')
plt.ylabel('Rozmiar opłaty')
plt.title('Wpływ czasu dnia na rozmiar opłaty')
plt.xticks(range(24))
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()


