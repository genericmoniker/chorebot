from setuptools import setup, find_packages

setup(
    name="chorebot",
    description="Household chores using Trello.",
    version="0.0.1",
    author="Eric Smith",
    author_email="eric@esmithy.net",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["py-trello", "APScheduler"],
)
