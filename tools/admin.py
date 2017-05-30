import uuid
import argparse
import datetime
from getpass import getpass

from dateutil.relativedelta import relativedelta
from passlib.apps import custom_app_context as pwd_context

from voat_sql.utils.user import UserUtils
from voat_sql.utils.db   import get_db

class Admin():
    def __init__(self):
        self.user_utils = UserUtils()
        self.db         = get_db()
        self.classes    = self.db.base.classes



    def add_admin(self, username, password):


        q = self.db.session.query(self.classes.user).filter(self.classes.user.username == username).first()

        if q:
            c = input('User already exists, this will delete the existing user. Continue?: [y/n] ')

            if c != 'y' and c != 'yes':
                return 

            else:
                self.db.session.delete(q)
                self.db.session.commit()

        one_month = datetime.datetime.utcnow() + relativedelta(months=1)

        new_admin = self.user_utils.create_user_object(password_hash=pwd_context.encrypt(password),
                                                       api_token=str(uuid.uuid4()),
                                                       registration_date=datetime.datetime.utcnow(),
                                                       username=username, 
                                                       verified=True, 
                                                       site_admin=True)
                                                       


        self.db.session.add(new_admin)

        if not self.db.session.commit():
            print('Admin added')
            return 

        print('Unable to add admin')



if __name__ == '__main__':

    a = Admin()

    parser = argparse.ArgumentParser(description='Voat administrative tool')
    
    parser.add_argument('--add-admin', dest='add_admin', action='store', help='--add-admin [username]')

    args = parser.parse_args()

    if args.add_admin:
        # make the user enter the password 2x to avoid typing errors.
        password1 = getpass('Password: ')
        password2 = getpass('Confirm Password: ')

        if password1 != password2:
            print('Passwords do not match')
            exit()

        a.add_admin(args.add_admin, password1)

