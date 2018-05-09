class Check:
    def __init__(self, msg):
        self.errors = []

        def get_amount():
            if ' ' in msg and len(msg.split(' ', 2)[1]) <= 1:
                errors.append('Amount is invalid')
                return None

            tmp = msg.split(' ', 2)[1]
            if not tmp.startswith('$'):
                errors.append('$ missing.')
                return None

            tmp = tmp.rstrip('0')
            tmp = tmp.lstrip('$')

            try:
                float(tmp)
            except ValueError:
                errors.append('Amount is not a number.')
                return None

            if '.' in tmp and len(tmp.split('.')) > 2:
                errors.append('Amount can only have two decimal places.')
                return None

            return float(tmp)

        #"Send $5 to John Snow (john.snow...
        def get_name():
            if 'to ' not in msg.split(' (')[0]:
                errors.append('Recipient is invalid')
            tmp = msg.split(' (', 1)[0]
            return tmp.split('to ', 1)[1]

        def get_email():
            if '(' not in msg or ')' not in msg:
                errors.append('No valid email found')
                return None
            #valid format: ...({email})...
            tmp = msg.split(')', 1)
            return tmp[0].split('(')[1]

        def get_description():
            #I could do an error check here, but descriptions could be optional.
            tmp = msg.split(') for ', 1)
            if len(tmp) >= 2:
                return tmp[1]

        self.amount = get_amount()
        self.name = get_name()
        self.email = get_email()
        self.description = get_description()

    def checkbook_post_data(self):
        if not self.errors:
            data = {"name":self.name,"recipient":self.email, "amount": self.amount}
            if self.description:
                data["description"] = self.description
            return data
        return None