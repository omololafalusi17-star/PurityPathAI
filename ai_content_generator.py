def generate_content(
    client,
    content_type,
    topic,
    audience,
    tone,
    model="gemini-3.6-flash",
):
    prompt = f"""
Create a high-quality educational resource for PurityPathAI.

Content type: {content_type}
Topic: {topic}
Audience: {audience}
Tone: {tone}

Requirements:
- Be age-appropriate and respectful.
- Avoid shame-based messaging.
- Focus on self-worth, healthy boundaries, safety, informed choices,
  and respectful relationships.
- Do not include sexually explicit content.
- Do not request personal information.
- If relevant, encourage trusted adult or professional support.
- Format the output with clear headings and useful bullet points.

You are a careful educational content creator for PurityPathAI.
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    return response.text