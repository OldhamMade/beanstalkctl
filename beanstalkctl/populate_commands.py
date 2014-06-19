import random
from .base import BaseCommand

PLACES = [
    'Aleksandrovka',
    'Aliabad',
    'Berezovka',
    'Buena Vista',
    'Buenavista',
    'Buenos Aires',
    'Cerro Colorado',
    'Cerro Negro',
    'El Carmen',
    'El Porvenir',
    'Gradina',
    'Hoseynabad',
    'Ivanovka',
    'Kamenka',
    'La Esperanza',
    'La Laguna',
    'La Palma',
    'Las Delicias',
    'Mikhaylovka',
    'Nikolayevka',
    'Ojo de Agua',
    'Quebrada Honda',
    'San Agustin',
    'San Antonio',
    'San Francisco',
    'San Isidro',
    'San Jose',
    'San Juan',
    'San Lorenzo',
    'San Luis',
    'San Martin',
    'San Miguel',
    'San Pablo',
    'San Pedro',
    'San Rafael',
    'San Vicente',
    'Santa Ana',
    'Santa Barbara',
    'Santa Cruz',
    'Santa Elena',
    'Santa Isabel',
    'Santa Lucia',
    'Santa Maria',
    'Santa Rita',
    'Santa Rosa',
    'Santa Teresa',
    'Santiago',
    'Santo Domingo',
    'Union',
]

COUNTRIES = [
    'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps',
    'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
    'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize',
    'Benin', 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil',
    'Brunei', 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon',
    'Canada', 'Cape Verde', 'Central African Rep', 'Chad', 'Chile', 'China',
    'Colombia', 'Comoros', 'Congo', 'Congo {Democratic Rep}', 'Costa Rica',
    'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti',
    'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt',
    'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia',
    'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana',
    'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana',
    'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran',
    'Iraq', 'Ireland {Republic}', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica',
    'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea North',
    'Korea South', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon',
    'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg',
    'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali',
    'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico',
    'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco',
    'Mozambique', 'Myanmar, {Burma}', 'Namibia', 'Nauru', 'Nepal',
    'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway',
    'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay',
    'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania',
    'Russian Federation', 'Rwanda', 'St Kitts & Nevis', 'St Lucia',
    'Saint Vincent & the Grenadines', 'Samoa', 'San Marino',
    'Sao Tome & Principe', 'Saudi Arabia',
    'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia',
    'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan',
    'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden',
    'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand',
    'Togo', 'Tonga', 'Trinidad & Tobago', 'Tunisia', 'Turkey', 'Turkmenistan',
    'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
    'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City',
    'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe',
]

STATES = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
    'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
    'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
    'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
    'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
    'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
    'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia',
    'Washington', 'West Virginia', 'Wisconsin', 'Wyoming',
]

NAMES = [
    'Jacob', 'Mason', 'William', 'Jayden', 'Noah', 'Michael', 'Ethan',
    'Alexander', 'Aiden', 'Daniel', 'Anthony', 'Matthew', 'Elijah', 'Joshua',
    'Liam', 'Andrew', 'James', 'David', 'Benjamin', 'Logan', 'Christopher',
    'Joseph', 'Jackson', 'Gabriel', 'Ryan', 'Samuel', 'John', 'Nathan', 'Lucas',
    'Christian', 'Jonathan', 'Caleb', 'Dylan', 'Landon', 'Isaac', 'Gavin',
    'Brayden', 'Tyler', 'Luke', 'Evan', 'Carter', 'Nicholas', 'Isaiah', 'Owen',
    'Jack', 'Jordan', 'Brandon', 'Wyatt', 'Julian', 'Aaron', 'Sophia',
    'Isabella', 'Emma', 'Olivia', 'Ava', 'Emily', 'Abigail', 'Madison', 'Mia',
    'Chloe', 'Elizabeth', 'Ella', 'Addison', 'Natalie', 'Lily', 'Grace',
    'Samantha', 'Avery', 'Sofia', 'Aubrey', 'Brooklyn', 'Lillian', 'Victoria',
    'Evelyn', 'Hannah', 'Alexis', 'Charlotte', 'Zoey', 'Leah', 'Amelia', 'Zoe',
    'Hailey', 'Layla', 'Gabriella', 'Nevaeh', 'Kaylee', 'Alyssa', 'Anna',
    'Sarah', 'Allison', 'Savannah', 'Ashley', 'Audrey', 'Taylor', 'Brianna',
    'Aaliyah', 'Riley', 'Camila', 'Khloe', 'Claire',
]


class PopulateCommand(BaseCommand):
    __cmd__ = 'populate'
    __help__ = 'not implemented'


class PopulateTubeCommand(PopulateCommand):
    __cmd__ = 'tube'
    __help__ = 'populate a tube with random jobs'

    def args(self):
        return self.beanstalkd.tubes()

    def run(self, line):
        args = line.split()

        if not len(args) == 3:
            print 'Please specify a tube'
            return

        tube = args[-1]

        if tube not in self.beanstalkd.tubes():
            print 'This will create a new tube named {0}'.format(tube)
            if not self.user_wants_to_continue():
                return

        count = raw_input('How many jobs would you like to create?\n')
        if not count.isdigit():
            print '{0} is not a number'.format(count)

        self.beanstalkd.use(tube)
        jids = [
            self.beanstalkd.put(
                '{0} visited {1}'.format(
                    random.choice(NAMES),
                    random.choice(PLACES),
                )
            )
            for i in range(int(count))
        ]

        print 'Created {0} jobs:\n  {1}'.format(len(jids), jids)


class PopulateTubesCommand(PopulateCommand):
    __cmd__ = 'tubes'
    __help__ = 'populate beanstalkd with random tubes and messages'

    def run(self, line):
        tube_count = raw_input('How many tubes would you like to create?\n')
        if not tube_count.isdigit():
            print '{0} is not a number'.format(tube_count)
            return

        job_count = raw_input('How many jobs would you like to create?\n')
        if not job_count.isdigit():
            print '{0} is not a number'.format(job_count)
            return

        tubes = [
            '{1}/{0}'.format(
                random.choice(PLACES),
                random.choice(STATES),
            ).replace(' ', '-').lower()
            for i in range(int(tube_count))
        ]

        for i in range(int(job_count)):
            self.beanstalkd.use(random.choice(tubes))
            self.beanstalkd.put(
                '{0} has visited'.format(
                    random.choice(NAMES),
                )
            )

        print 'Created {0} job{1} across {2} tube{3}.'.format(
            job_count,
            '' if job_count is 1 else 's',
            tube_count,
            '' if tube_count is 1 else 's',
        )
