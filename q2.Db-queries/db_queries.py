import mysql.connector
from tabulate import tabulate

conn = mysql.connector.connect(
    host='mysql-rfam-public.ebi.ac.uk',
    port=4497,
    user='rfamro',
    password='',
    database='Rfam'
)

cursor = conn.cursor()

print("=" * 80)
print("QUESTION (a): Tigers in Taxonomy")
print("=" * 80)

cursor.execute("""
    SELECT COUNT(*) as tiger_count
    FROM taxonomy
    WHERE species LIKE '%Panthera tigris%'
       OR tax_string LIKE '%Panthera tigris%'
""")
result = cursor.fetchall()
print(f"\nNumber of tiger types found: {result[0][0]}")

cursor.execute("""
    SELECT ncbi_id, species, tax_string
    FROM taxonomy
    WHERE tax_string LIKE '%Panthera tigris sumatrae%'
       OR species LIKE '%sumatrae%'
    LIMIT 5
""")
result = cursor.fetchall()
print("\nSumatran Tiger Information:")
print(tabulate(result, headers=['NCBI ID', 'Species', 'Tax String'], tablefmt='grid'))

print("\n" + "=" * 80)
print("QUESTION (b): Foreign Key Relationships")
print("=" * 80)

relationships = [
    ['rfamseq', 'taxonomy', 'ncbi_id'],
    ['full_region', 'rfamseq', 'rfamseq_acc'],
    ['full_region', 'family', 'rfam_acc'],
    ['clan_membership', 'family', 'rfam_acc'],
    ['clan_membership', 'clan', 'clan_acc']
]
print("\nTables and their connecting columns:")
print(tabulate(relationships, headers=['Table 1', 'Table 2', 'Join Column'], tablefmt='grid'))

print("\n" + "=" * 80)
print("QUESTION (c): Rice with Longest DNA Sequence")
print("=" * 80)

cursor.execute("""
    SELECT 
        t.species,
        t.ncbi_id,
        rs.rfamseq_acc,
        rs.length as sequence_length
    FROM 
        (
            SELECT DISTINCT ncbi_id, species
            FROM taxonomy
            WHERE species LIKE 'Oryza%'
               OR species LIKE '%Oryza %'
               OR tax_string LIKE '%Oryza%'
        ) t
    JOIN 
        rfamseq rs ON t.ncbi_id = rs.ncbi_id
    ORDER BY 
        rs.length DESC
    LIMIT 1
""")
result = cursor.fetchall()
print("\nRice species with longest DNA sequence:")
print(tabulate(result, headers=['Species', 'NCBI ID', 'Sequence Acc', 'Length (bp)'], tablefmt='grid'))

print("\n" + "=" * 80)
print("QUESTION (d): Page 9 - Families with DNA Length > 1,000,000")
print("=" * 80)

cursor.execute("""
    SELECT 
        f.rfam_acc as family_accession,
        f.rfam_id as family_name,
        family_max.max_length as max_dna_length
    FROM 
        family f
    JOIN (
        SELECT 
            fr.rfam_acc,
            MAX(long_seqs.length) as max_length
        FROM 
            full_region fr
        JOIN (
            SELECT rfamseq_acc, length
            FROM rfamseq
            WHERE length > 1000000
        ) long_seqs ON fr.rfamseq_acc = long_seqs.rfamseq_acc
        GROUP BY 
            fr.rfam_acc
    ) family_max ON f.rfam_acc = family_max.rfam_acc
    ORDER BY 
        family_max.max_length DESC
    LIMIT 15 OFFSET 120
""")
result = cursor.fetchall()
print("\nPage 9 Results (15 per page, records 121-135):")
print(tabulate(result, headers=['Family Accession', 'Family Name', 'Max DNA Length (bp)'], tablefmt='grid'))

cursor.execute("""
    SELECT COUNT(DISTINCT fr.rfam_acc) as total_families
    FROM 
        full_region fr
    WHERE 
        fr.rfamseq_acc IN (
            SELECT rfamseq_acc 
            FROM rfamseq 
            WHERE length > 1000000
        )
""")
result = cursor.fetchall()
print(f"\nTotal families with sequences > 1M: {result[0][0]}")
print(f"Total pages (15 per page): {(result[0][0] + 14) // 15}")

cursor.close()
conn.close()
