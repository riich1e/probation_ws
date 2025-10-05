from setuptools import find_packages, setup

package_name = 'solution_pkg'

setup(
    name="solution_pkg",
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']), ('share/' + package_name + '/launch', [
		'launch/solution_launch.py',]),  
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Fakhri Rasyiid',
    maintainer_email='throwawaypeas976@gmail.com',
    description='Solution to Probation task, Obstacle Avoidance not attempted',
    license='Apache License 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
           'nav_publisher = solution_pkg.nav_publisher:main',
	   'depth_maintain_publisher = solution_pkg.depth_maintain_publisher:main',
	   'set_mode_client = solution_pkg.set_mode_client:main',
        ],
    },
)
