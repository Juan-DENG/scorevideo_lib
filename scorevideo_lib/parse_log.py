class Log:

    @staticmethod
    def get_section_header(log_file):
        header = []
        for i in range(2):
            header.append(log_file.readline())
        return header

    @staticmethod
    def get_section_video_info(log_file):
        pass

    @staticmethod
    def get_section_commands(log_file):
        pass

    @staticmethod
    def get_section_raw(log_file):
        pass

    @staticmethod
    def get_section_full(log_file):
        pass

    @staticmethod
    def get_section_notes(log_file):
        pass

    @staticmethod
    def get_section_marks(log_file):
        pass