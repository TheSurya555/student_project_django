from aboutUs.models import AboutUsContent

default_about_us = AboutUsContent.objects.create(
    title="Default About Us",
    description="This is the default About Us content.",
    image="about_us/talentsprout.jpeg"
)

print(default_about_us.id)


from aboutUs.models import TeamMember

default_about_us_id = default_about_us.id
TeamMember.objects.filter(about_us__isnull=True).update(about_us=default_about_us_id)
