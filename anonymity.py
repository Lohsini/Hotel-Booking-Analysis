from typing import Counter, List, Optional
from collections import defaultdict
import os
import csv


class Attribute:
    def __init__(self, max_level: int, value):
        self.value = value if value else "*"
        self.generalization_value = "*"
        self.generalization_level = 0
        self.max_level = max_level if max_level else 0
        self.distortion = 0.0
        self.precision = 0.0
        self._set_qualifiers()

    def _set_qualifiers(self):  # for the attribute itself
        factor = self.generalization_level / self.max_level
        if factor < 0:
            return
        self.precision = factor
        if self.value:
            self.generalization_value = self._get_value()
        self.distortion = factor / 4

    def __eq__(self, other: object) -> bool:  # check equal
        if not self.generalization_value:
            return not other.generalization_value
        return other and other.generalization_value == self.generalization_value

    def set_generalization_level(self, level: int):
        if level:
            minLevel = min(level, self.max_level)
            self.generalization_level = max(0, minLevel)
            self._set_qualifiers()

    def add_generalization_level(self):
        if self.generalization_level < 0:
            exit(1)
        else:
            self.set_generalization_level(self.generalization_level + 1)

    def reduce_generalization_level(self):
        if self.generalization_level < 0:
            exit(1)
        else:
            self.set_generalization_level(self.generalization_level - 1)

    def get_value(self):
        if self:
            return self.generalization_value

    def _get_value(self):
        if self:
            return self.value


class Age(Attribute):
    def __init__(self, age: str):
        max_level = 4
        if age:
            super().__init__(max_level, int(age))  # max_level, value

    def _get_value(self) -> str:
        if self.generalization_level == 1:  # <18 / 18-34 / 35-49 / 50-64 / 65+
            if self.value < 18:
                return "<18"
            elif self.value >= 18 and self.value <= 34:
                return "18-34"
            elif self.value >= 35 and self.value <= 49:
                return "35-49"
            elif self.value >= 50 and self.value <= 64:
                return "50-64"
            elif self.value >= 65:
                return ">=65"
        elif self.generalization_level == 0:  # real age
            return str(self.value)
        elif self.generalization_level == 2:  # Children / Adults / Elderly
            if self.value < 18:
                return "Children"
            elif self.value >= 18 and self.value <= 64:
                return "Adults"
            elif self.value >= 65:
                return "Elderly"
        elif self.generalization_level == 3:  # Underage / Adults
            if self.value <= 64:
                return "Underage"
            elif self.value >= 65:
                return "Adults"
        else:
            return "*"


class Country(Attribute):
    def __init__(self, country: str):
        max_level = 4
        if country:
            super().__init__(max_level, country)  # max_level, value

    def _get_value(self):
        if self.generalization_level == 0:  # Real country code
            return self.value
        elif self.generalization_level == 1:  # Regions
            for region, countries_list in self._get_regions().items():
                if self.value in countries_list:
                    return region
        elif self.generalization_level == 2:  # Continents
            region = self._get_value(generalization_level=1)
            return self._get_continent(region)
        elif self.generalization_level == 3:  # East or West
            region = self._get_value(generalization_level=1)
            continent = self._get_value(generalization_level=2)
            return self._get_east_west(region, continent)
        return "*"

    def _get_regions(self):
        return {
            "East Asia": ['CHN', 'JPN', 'KOR', 'PRK', 'TWN', 'HKG', 'MAC', 'MNG'],
            "Southeast Asia": ['IDN', 'VNM', 'THA', 'PHL', 'MYS', 'SGP', 'MMR', 'KHM', 'LAO', 'BRN', 'TLS'],
            "South Asia": ['IND', 'PAK', 'BGD', 'NPL', 'LKA', 'MDV', 'BTN'],
            "Northeast Asia": ['RUS', 'MNG', 'PRK', 'JPN', 'KOR', 'CHN'],
            "Central Asia": ['KAZ', 'UZB', 'KGZ', 'TKM', 'TJK'],
            "West Asia": ['AFG', 'IRN', 'IRQ', 'SYR', 'JOR', 'LBN', 'ISR', 'PSE', 'KWT', 'OMN', 'QAT', 'SAU', 'ARE', 'YEM', 'BHR'],
            "Eastern Europe": ['RUS', 'UKR', 'POL', 'ROU', 'CZE', 'HUN', 'BLR', 'BGR', 'SVK', 'LTU', 'HRV', 'SVN', 'EST', 'LVA'],
            "Western Europe": ['DEU', 'FRA', 'GBR', 'ITA', 'ESP', 'NLD', 'BEL', 'AUT', 'CHE', 'LUX', 'IRL', 'PRT', 'DNK', 'NOR', 'SWE', 'FIN', 'ISL', 'GRC'],
            "East Africa": ['ETH', 'SDN', 'UGA', 'KEN', 'TZA', 'MOZ', 'BDI', 'ZMB', 'RWA', 'MWI', 'MDG', 'ERI', 'SOM', 'GAB'],
            "West Africa": ['NGA', 'GHA', 'CIV', 'SEN', 'CMR', 'BFA', 'NER', 'MLI', 'TCD', 'GNB', 'GIN', 'CIV', 'TGO', 'BEN', 'LBR', 'SLE', 'GMB', 'BFA'],
            "Southern Africa": ['ZAF', 'AGO', 'ZMB', 'ZWE', 'MWI', 'NAM', 'BWA', 'LSO', 'SWZ'],
            "Central Africa": ['COD', 'CAF', 'TCD', 'AGO', 'CMR', 'GIN', 'ZAF', 'ZMB', 'TZA'],
            "North America": ['USA', 'CAN', 'MEX', 'BLZ', 'CRI', 'SLV', 'GTM', 'HND', 'NIC', 'PAN'],
            "South America": ['BRA', 'ARG', 'COL', 'PER', 'VEN', 'CHL', 'ECU', 'BOL', 'PRY', 'URY'],
            "Oceania": ['AUS', 'NZL', 'PNG', 'FJI', 'SLB', 'VUT', 'PLW', 'KIR', 'TUV', 'WSM'],
            "Antarctica": ['ATA']
        }

    def _get_continent(self, region):
        continents = {
            'Asia': ['East Asia', 'Southeast Asia', 'South Asia', 'Northeast Asia', 'Central Asia', 'West Asia'],
            'Europe': ['Eastern Europe', 'Western Europe'],
            'Africa': ['East Africa', 'West Africa', 'Southern Africa', 'Central Africa'],
            'North America': ['North America'],
            'South America': ['South America'],
            'Oceania': ['Oceania'],
            'Antarctica': ['Antarctica']
        }
        for continent, regions_list in continents.items():
            if region in regions_list:
                return continent
        return "Unknown"

    def _get_east_west(self, region, continent):
        east_west = {
            'Eastern': ['East Asia', 'Southeast Asia', 'South Asia', 'Northeast Asia', 'Central Asia', 'Eastern Europe', 'West Asia'],
            'Western': ['Western Europe', 'East Africa', 'West Africa', 'Southern Africa', 'Central Africa', 'North America', 'South America', 'Oceania', 'Antarctica']
        }
        if region in east_west['Eastern'] and continent != 'Africa':
            return 'Eastern'
        elif region in east_west['Western'] and continent != 'Oceania':
            return 'Western'
        return "Unknown"


class StayNight(Attribute):
    def __init__(self, stay_night: str):
        max_level = 3
        if stay_night:
            super().__init__(max_level, int(stay_night))  # max_level, value

    def _get_value(self) -> str:
        if self.generalization_level == 1:
            if self.value == "*":
                return "*"
            elif self.value == 0:
                return "First-Time Guests"
            elif self.value >= 1 and self.value <= 3:
                return "Rare Guests"
            elif self.value >= 4 and self.value <= 12:
                return "Occasional Guests"
            elif self.value >= 13:
                return "Frequent Guests"
        elif self.generalization_level == 0:  # real stay day
            return str(self.value)
        elif self.generalization_level == 2:
            if self.value < 2:
                return "Never visit"
            elif self.value >= 2:
                return "Ever visit"
        else:
            return "*"


curId = 0


class User:

    def __init__(
        self,
        hotel,
        is_canceled,
        lead_time,
        arrival_date_year,
        arrival_date_month,
        arrival_date_week_number,
        arrival_date_day_of_month,
        stays_in_weekend_nights,
        stays_in_week_nights: str,
        adults,
        children,
        babies,
        meal,
        country: str,
        market_segment,
        distribution_channel,
        is_repeated_guest,
        previous_cancellations,
        previous_bookings_not_canceled,
        reserved_room_type,
        assigned_room_type,
        booking_changes,
        deposit_type,
        agent,
        company,
        days_in_waiting_list,
        customer_type,
        adr,
        required_car_parking_spaces,
        total_of_special_requests,
        reservation_status,
        reservation_status_date: str,
        name: str,
        email,
        phone_number,
        credit_card,
        age: str
    ):
        self.userSet = None
        self.groupedVisitationDate: Optional[Counter[str]] = None
        self.age = Age(age)
        self.country = Country(country)
        self.visitation_date = reservation_status_date
        self.stay_night = StayNight(stays_in_week_nights)
        self.initialize_sets()
        self.name = name

        # for k-anonymity
        self.min_k = 10

        global curId

        self.curId = curId
        curId += 1

        self.count = 1

    def __eq__(self, other) -> bool:  # check equal
        return bool(other and
                    self.min_k == other.min_k and
                    self.age == other.age and
                    self.country == other.country and
                    self.stay_night == other.stay_night)

    def __hash__(self) -> int:  # check equal
        return curId

    def attributes(self):
        return [self.age, self.country, self.stay_night]

    def getDistortion(self) -> float:
        results = []
        for attr in self.attributes():
            if attr:
                results.append(attr.distortion)
            else:
                return 0
        return sum(results)

    def getPrecision(self) -> int:
        results = []
        for attr in self.attributes():
            if attr:
                results.append(attr.precision)
            else:
                return 0
        return sum(results) * self.count

    def merge_user(self, user) -> bool:
        if self == user:
            self.count += user.count
            if not user or not user.groupedVisitationDate:
                return False

            self.groupedVisitationDate.update(user.groupedVisitationDate)

            if not user.userSet:
                return False

            self.userSet = self.userSet.union(user.userSet)

            if user.initialize_sets:
                user.initialize_sets()
            return True
        return False

    def initialize_sets(self):
        if self.userSet and self.count == 1:
            return
        info = {self.visitation_date: 1}
        self.groupedVisitationDate = Counter(info)
        if self:
            self.userSet = set([self])
            self.count = 1

    def satisfied_k(self) -> bool:
        if not self:
            return 0
        return not self.count < self.min_k

    def is_fully_generalized(self):
        for attr in self.attributes():
            if attr.generalization_level != attr.max_level:
                return False
        return True

    def diverseAttr(self):
        max = 1
        attribute = None
        for attr in self.attributes():
            if not attr:
                return 0
            if attr.distortion <= max:
                if attr.distortion:
                    max = attr.distortion
                attribute = attr
        return attribute

    def basicStr(self) -> str:
        self_info = []
        self_info.append(f"{self.visitation_date}")
        self_info.append(f"{self.age.get_value()}")
        self_info.append(f"{self.country.get_value()}")
        self_info.append(f"{self.stay_night.get_value()}")
        return self_info

    def _oriStr(self) -> str:
        self_info = []
        self_info.append(f"{self.visitation_date}")
        self_info.append(f"{self.age.value}")
        self_info.append(f"{self.country.value}")
        self_info.append(f"{self.stay_night.value}")
        return self_info

    def oriStr(self):
        userSet = list(self.userSet)
        userSet.sort(key=lambda x: x.visitation_date)

        self_info = []

        for user in userSet:
            if user:
                self_info = user._oriStr()
        return self_info


dest = "dest"


def ensureDest(prefix):
    path = "result"
    os.makedirs(path, exist_ok=True)
    return path


def generalizeUsers(users):
    N = len(users)
    last = N + 1
    run = True
    idx = 0
    while run:
        idx += 1
        run = False
        groupedUsers = []
        workingList: List[User] = users.copy()
        while not len(workingList) == 0:
            u = workingList.pop()

            if u.is_fully_generalized():
                generalized += u.count
                continue

            for i, user in enumerate(workingList):
                if not u.merge_user(user):
                    pass
                # else:
                #     workingList[i] = None
            if u:
                groupedUsers.append(u)

        if len(groupedUsers) == last:  # nothing change
            users = groupedUsers
            break
        last = len(groupedUsers)

        for user in groupedUsers:
            if not user.satisfied_k():  # check k
                for attr in user.attributes():
                    attr.add_generalization_level()
                run = True
        users = groupedUsers

    total = getUserCount(users)
    return users


def remove_unsatisfied_users(users: List[User]) -> list:
    combination_users = defaultdict(list)
    for user in users:
        combination = (user.age.get_value(), user.country.get_value(),
                       user.stay_night.get_value())
        combination_users[combination].append(user)
    for combination, user_list in combination_users.items():
        if len(user_list) > user.min_k:
            continue
        for user in user_list:
            users.remove(user)
    return users


def getUserCount(users: List[User]) -> int:
    return sum([user.count for user in users if user])


def print_users_to_files(header: List[str], raw: List[User], final: List[User]):
    path = ensureDest("result")

    before_num = len(raw)
    print_raw_users(header, raw, path)

    after_num = len(final)
    print_final_users(header, final, path)

    removed_num = before_num - after_num
    print(f"Init Total users: {before_num}")
    print(f"\n{removed_num} unsatisfied users were removed")
    print(f"Final Total users: {after_num}")
    percentage = round((100 * after_num) / before_num, 2)
    print(f"\nUser utility: {after_num}/{before_num} : {percentage}%")


def print_raw_users(header: List[str], raw: List[User], path: str):
    output = []
    for user in raw:
        if user:
            output.append(user.oriStr())
    filepath = os.path.join(path, "input.csv")
    with open(filepath, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(output)


def print_final_users(header: List[str], final: List[User], path: str):
    output = []
    for user in final:
        result = user.basicStr()
        output.append(result)
    sorted_objects = sorted(output, key=lambda x: (x[1], x[2], x[3], x[0]))
    filepath = os.path.join(path, "output.csv")
    with open(filepath, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(sorted_objects)


def read_raw_data(file_path):
    users = []
    header = ["Visitation Date", "Age", "Country",
              "Number of overnight stays"]
    with open(file_path, newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            user_info_list = []
            for field in row:
                if field != "":
                    user_info_list.append(field.strip())
                else:
                    user_info_list.append("*")
            user = User(*user_info_list)
            users.append(user)
    return users, header


def getDistortion(users: List[User]) -> float:
    nums = []
    for user in users:
        if not user:
            break
        nums.append(user.getDistortion())
    return round(sum(nums) / len(users), 4) if len(nums) > 0 else 0.0


def getPrecision(users: List[User]) -> float:
    nums = []
    result = 0.0
    for user in users:
        if not user:
            break
        nums.append(user.getPrecision())
    userCount = getUserCount(users)
    result = round(1 - (sum(nums) / (userCount * 4)), 4)  # 0.0000
    return result


def main():
    raw_users_list, header = read_raw_data(
        "./modified_data/hotel_booking_simple(+age).csv"
    )
    processed_users_list = generalizeUsers(raw_users_list.copy())
    final_users_list = remove_unsatisfied_users(processed_users_list)
    print_users_to_files(header, raw_users_list, final_users_list)


if __name__ == "__main__":
    main()
