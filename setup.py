from setuptools import setup, find_packages
import src


if __name__ == '__main__':
    setup(name='role_crawl',
          version=src.version,
          description="role_crawl",
          long_description="""\
              """,
          classifiers=[],
          keywords='',
          author='',
          author_email='',
          url='',
          license='',
          zip_safe=False,
          include_package_data=True,
          packages=find_packages(exclude=["tests"]),
          install_requires=[
          ]
    )
