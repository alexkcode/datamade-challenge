import os, csv, requests
from datetime import date

class LegislatorProcessor:

    def __init__(self):
        if not os.path.exists('legislators.csv'):
            self.download_data()
        self.data = self.get_data('legislators.csv')

    def download_data(self):
        url = 'http://unitedstates.sunlightfoundation.com/legislators/legislators.csv'
        open('legislators.csv', 'wb').write(requests.get(url).content)

    def get_data(self, filepath):
        with open(filepath) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            return list(reader)

    def get_young_dems(self):
        """Return filter object of all Democrats who are younger than 45 years old"""
        is_democrat = lambda row: row['party'] == 'D'
        is_young = lambda row: date.today().year - date.fromisoformat(row['birthdate']).year < 45
        democrats = filter(is_young and is_democrat, self.data)
        return list(democrats)
            
    def get_social_reps(self):
        """Return filter object of all Republicans who have Twitter accounts and YouTube channels"""
        is_republican = lambda row: row['party'] == 'R'
        is_social = lambda row: row['twitter_id'].strip() and row['youtube_url'].strip()
        republicans = filter(is_republican and is_social, self.data)
        return list(republicans)

    def write_data(self, filepath, data):
        with open(filepath, mode='w', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            csvwriter.writeheader()
            csvwriter.writerows(data)

def main():
    legis_filter = LegislatorProcessor()
    legis_filter.write_data('democrats.csv', legis_filter.get_young_dems())
    legis_filter.write_data('republicans.csv', legis_filter.get_social_reps())

if __name__ == "__main__":
    main()