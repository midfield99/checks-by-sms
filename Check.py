class Check:
    @staticmethod
    def __get_substr(msg, start, end):
        #helper method for message processing.
        # returns substring between start and end
        # returns None if substring does not exist
        try:
            tmp = msg.split(start)[1]
            if end in tmp:
                tmp = tmp.split(end)[0]
                return tmp if tmp != '' else None
            return None
        except IndexError:
            return None

    def __init__(self, msg):
        self.errors = []
        self.valid_format = 'Send ${amount} to {name} ({email}) for {description}'

        #put general formatting checks here
        def general_format_check():
            if not msg.startswith('Send'):
                self.errors.append('Start message with "Send"')

        def get_amount():
            tmp = Check.__get_substr(msg, ' $', ' ')
            if not tmp:
                self.errors.append('Invalid amount.')
                return None

            try:
                float(tmp)
            except ValueError:
                self.errors.append('Amount is not a number.')
                return None

            if '.' in tmp:
                tmp = tmp.rstrip('0')
                if len(tmp.split('.')[1]) > 2:
                    self.errors.append('Amount can only have two decimal places.')
                return None

            return float(tmp)

        #"Send $5 to John Snow (john.snow...
        def get_name():
            tmp = Check.__get_substr(msg, 'to ', ' (')
            if not tmp:
                self.errors.append("Invalid name")
                return None
            return tmp

        def get_email():
            #valid format: ...({email})...
            tmp = Check.__get_substr(msg, ' (', ') ')
            if not tmp:
                self.errors.append("Invalid email")
                return None
            return tmp

        def get_description():
            #I could do an error check here, but descriptions could be optional.
            tmp = msg.split(') for ', 1)
            if len(tmp) >= 2:
                return tmp[1]

        general_format_check()
        self.amount = get_amount()
        self.name = get_name()
        self.email = get_email()
        self.description = get_description()

        if self.errors:
            self.errors.append('Format is:' + self.valid_format)

    def checkbook_post_data(self):
        if not self.errors:
            data = {"name":self.name,"recipient":self.email, "amount": self.amount}
            if self.description:
                data["description"] = self.description
            return data
        return None
