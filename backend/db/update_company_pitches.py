"""
Updates all outreach campaigns in SQLite with bespoke, company-profile-tailored
Email Pitches and LinkedIn Notes for all 112 contacts.
"""

import sqlite3
import uuid
from backend.agents.company_profiles import generate_tailored_email, generate_tailored_linkedin

def update_all_pitches():
    conn = sqlite3.connect('data/ai7_career.db')
    conn.row_factory = sqlite3.Row
    
    # Clean any unicode dashes in jobs
    for j in conn.execute('SELECT id, title FROM jobs').fetchall():
        clean_title = j['title'].replace('—', '-').replace('–', '-')
        if clean_title != j['title']:
            conn.execute('UPDATE jobs SET title = ? WHERE id = ?', (clean_title, j['id']))
    conn.commit()

    contacts = conn.execute('SELECT * FROM contacts').fetchall()
    print(f'Total contacts to process: {len(contacts)}')

    updated = 0
    for c in contacts:
        c_dict = dict(c)
        job = conn.execute('SELECT * FROM jobs WHERE company_name = ? LIMIT 1', (c_dict['company_name'],)).fetchone()
        job_dict = dict(job) if job else None

        email_data = generate_tailored_email(c_dict, job_dict)
        linkedin_note = generate_tailored_linkedin(c_dict, job_dict)

        existing = conn.execute('SELECT id, status FROM outreach_campaigns WHERE contact_id = ?', (c_dict['id'],)).fetchone()
        if existing:
            conn.execute('''
                UPDATE outreach_campaigns 
                SET subject = ?, message_body = ?, linkedin_note = ?, company_name = ?
                WHERE contact_id = ?
            ''', (email_data['subject'], email_data['body'], linkedin_note, c_dict['company_name'], c_dict['id']))
        else:
            outreach_id = f"out_{str(uuid.uuid4())[:8]}"
            conn.execute('''
                INSERT INTO outreach_campaigns (id, job_id, contact_id, company_name, channel, subject, message_body, linkedin_note, outreach_type, status)
                VALUES (?, ?, ?, ?, 'EMAIL', ?, ?, ?, 'HIRING_MGR_PITCH', 'DRAFT')
            ''', (outreach_id, job_dict['id'] if job_dict else None, c_dict['id'], c_dict['company_name'], email_data['subject'], email_data['body'], linkedin_note))
        updated += 1

    conn.commit()
    print(f'Successfully updated {updated} outreach campaigns with company profiles!')

    sample1 = conn.execute("""
        SELECT c.company_name, c.full_name, o.subject, o.message_body, o.linkedin_note 
        FROM contacts c JOIN outreach_campaigns o ON c.id = o.contact_id 
        WHERE c.company_name = 'Brookfield Asset Management' LIMIT 1
    """).fetchone()
    print("\n--- BROOKFIELD SAMPLE EMAIL ---")
    print("Subject:", sample1["subject"])
    print("Body Preview:\n", sample1["message_body"][:350] + "...")
    print("\n--- BROOKFIELD SAMPLE LINKEDIN ---")
    print(sample1["linkedin_note"])

    sample2 = conn.execute("""
        SELECT c.company_name, c.full_name, o.subject, o.message_body, o.linkedin_note 
        FROM contacts c JOIN outreach_campaigns o ON c.id = o.contact_id 
        WHERE c.company_name = 'Emaar Properties' LIMIT 1
    """).fetchone()
    print("\n--- EMAAR SAMPLE EMAIL ---")
    print("Subject:", sample2["subject"])
    print("Body Preview:\n", sample2["message_body"][:350] + "...")
    print("\n--- EMAAR SAMPLE LINKEDIN ---")
    print(sample2["linkedin_note"])

if __name__ == "__main__":
    update_all_pitches()
