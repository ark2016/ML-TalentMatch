f = open("name.pdf")

answer = {
  "resume": {
      "resume_id": resume_id,
      "first_name": first_name,
      "last_name": last_name,
      "middle_name": middle_name,
      "birth_date": birth_date,
      "birth_date_year_only": birth_date_year_only,
      "country": country,
      "city": city,
      "about": about,
      "key_skills": key_skills,
      "salary_expectations_amount": salary_expectations_amount,
      "salary_expectations_currency": salary_expectations_currency,
      "photo_path": photo_path,
      "gender": gender,
      "language": language,
      "resume_name": resume_name,
      "source_link": source_link,
      "contactItems": [
        {
          "resume_contact_item_id": resume_contact_item_id,
          "value": value,
          "comment": comment,
          "contact_type": contact_type
        }
      ],
      "educationItems": [
        {
          "resume_education_item_id": resume_education_item_id,
          "year": year,
          "organization": organization,
          "faculty": faculty,
          "specialty": specialty,
          "result": result,
          "education_type": education_type,
          "education_level": education_level
        }
      ],
      "experienceItems": [
        {
          "resume_experience_item_id": resume_experience_item_id,
          "starts": starts,
          "ends": ends,
          "employer": employer,
          "city": city,
          "url": url,
          "position": position,
          "description": description,
          "order": order
        }
      ],
      "languageItems": [
        {
          "resume_language_item_id": resume_language_item_id,
          "language": language,
          "language_level": language_level
        }
      ]
    }
}
