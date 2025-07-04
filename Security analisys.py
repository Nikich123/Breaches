import pandas as pd


# Завантаження набору даних
print("Завантаження даних...")
df = pd.read_csv('breaches.csv')


print("\nРозмір початкового набору даних:", df.shape)
print("\nПерші 5 рядків даних:")
print(df.head())
print("\nІнформація про типи даних:")
print(df.info())


print("\nКількість пропущених значень у кожному стовпці:")
print(df.isnull().sum())


duplicates = df.duplicated()
duplicate_count = duplicates.sum()
print(f"\nКількість дублікатів: {duplicate_count}")


print("\nКатегорійні стовпці та унікальні значення:")
categorical_columns = df.select_dtypes(include=['object']).columns
for col in categorical_columns:
    unique_values = df[col].nunique()
    print(f"{col}: {unique_values} унікальних значень")
    if unique_values < 20:
        print(df[col].unique())

# Очищення даних


print("\nКонвертація 'records lost' до числового формату...")
if 'records lost' in df.columns:

    print("Приклади записів у стовпці 'Rrecords lost' перед очищенням:")
    print(df['records lost'].head(10))


    df['records lost'] = df['records lost'].astype(str).str.replace(',', '')
    df['records lost'] = pd.to_numeric(df['records lost'], errors='coerce')


if 'year   ' in df.columns:
    print("\nКонвертація 'year   ' до числового формату...")
    df['Year'] = pd.to_numeric(df['year   '], errors='coerce')


date_columns = [col for col in df.columns if 'date' in col.lower() or 'date' in col]
for col in date_columns:
    print(f"\nКонвертація стовпця '{col}' до формату дати...")
    df[col] = pd.to_datetime(df[col], errors='coerce')


critical_columns = []
if 'organisation' in df.columns:
    critical_columns.append('organisation')
if 'records lost' in df.columns:
    critical_columns.append('records lost')

if critical_columns:
    print(f"\nВидалення рядків з пропущеними значеннями у критичних стовпцях: {critical_columns}")
    df_cleaned = df.dropna(subset=critical_columns)
    print(f"Видалено {df.shape[0] - df_cleaned.shape[0]} рядків з пропущеними критичними даними")
    df = df_cleaned


print("\nВидалення дублікатів...")
df_no_duplicates = df.drop_duplicates()
print(f"Видалено {df.shape[0] - df_no_duplicates.shape[0]} дублікатів")
df = df_no_duplicates


print("\nРозмір очищеного набору даних:", df.shape)
print("\nПеревірка відсутніх значень після очищення:")
print(df.isnull().sum())


clean_file_path = 'breaches_cleaned.csv'
df.to_csv(clean_file_path, index=False)
print(f"\nОчищені дані збережено у файл: {clean_file_path}")


print("\nПриклад очищених даних:")
print(df.head())


if 'sector' in df.columns:
    print("\nРозподіл за секторами:")
    print(df['sector'].value_counts().head(10))


if 'year   ' in df.columns:
    print("\nКількість витоків за роками:")
    year_counts = df['year   '].value_counts().sort_index()
    print(year_counts)


method_columns = [col for col in df.columns if 'method' in col.lower() or 'Method' in col]
for col in method_columns:
    print(f"\nРозподіл за методами злому ({col}):")
    print(df[col].value_counts().head(10))

print("\nОчищення даних завершено успішно!")