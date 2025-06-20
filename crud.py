from sqlalchemy.orm import Session
from models import Contact, LinkPrecedenceEnum
from schemas import IdentifyResponse
from typing import Optional

def handle_identify_logic(db: Session, email: Optional[str], phone: Optional[str]) -> IdentifyResponse:
    # Step 1: Match by email and phone independently
    email_matches = []
    phone_matches = []

    if email:
        email_matches = db.query(Contact).filter(Contact.email == email).all()

    if phone:
        phone_matches = db.query(Contact).filter(Contact.phoneNumber == phone).all()

    # Step 2: Combine and deduplicate matches
    matched_contacts = list({c.id: c for c in email_matches + phone_matches}.values())

    if not matched_contacts:
        # Case 1: No match → create a new primary contact
        new_contact = Contact(
            email=email,
            phoneNumber=phone,
            linkPrecedence=LinkPrecedenceEnum.primary
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)

        return IdentifyResponse(
            primaryContactId=new_contact.id,
            emails=[email] if email else [],
            phoneNumbers=[phone] if phone else [],
            secondaryContactIds=[]
        )

    # Step 3: Find the earliest 'primary' contact
    primary_contacts = [c for c in matched_contacts if c.linkPrecedence == LinkPrecedenceEnum.primary]

    if primary_contacts:
        primary_contact = sorted(primary_contacts, key=lambda x: x.createdAt)[0]
    else:
        # Fallback: all are secondary → get the linked primary
        secondary = sorted(matched_contacts, key=lambda x: x.createdAt)[0]
        primary_contact = db.query(Contact).filter(Contact.id == secondary.linkedId).first()

    # Step 4: Get all contacts linked to this primary
    all_related_contacts = db.query(Contact).filter(
        (Contact.id == primary_contact.id) | (Contact.linkedId == primary_contact.id)
    ).all()

    # Step 5: Check if incoming email/phone is new
    existing_emails = {c.email for c in all_related_contacts if c.email}
    existing_phones = {c.phoneNumber for c in all_related_contacts if c.phoneNumber}

    needs_new_entry = (email and email not in existing_emails) or (phone and phone not in existing_phones)

    if needs_new_entry:
        new_contact = Contact(
            email=email,
            phoneNumber=phone,
            linkedId=primary_contact.id,
            linkPrecedence=LinkPrecedenceEnum.secondary
        )
        db.add(new_contact)
        db.commit()

    # Step 6: Final response set
    final_contacts = db.query(Contact).filter(
        (Contact.id == primary_contact.id) | (Contact.linkedId == primary_contact.id)
    ).all()

    emails = sorted({c.email for c in final_contacts if c.email})
    phones = sorted({c.phoneNumber for c in final_contacts if c.phoneNumber})
    secondary_ids = sorted([c.id for c in final_contacts if c.linkPrecedence == LinkPrecedenceEnum.secondary])

    return IdentifyResponse(
        primaryContactId=primary_contact.id,
        emails=emails,
        phoneNumbers=phones,
        secondaryContactIds=secondary_ids
    )
