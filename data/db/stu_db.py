from dao.base import BaseDao
from entity import Student

class StuDao(BaseDao):
    def query(self, where=None, args=None):
        ret = super(StuDao, self).query('student', 'sn', 'name', 'age', 'sex', where=where, args=args)
        return [
            Student(item['sn'], item['name'], item['age'], item['sex'])
            for item in ret
        ]



if __name__ == "__main__":
    dao = StuDao()
    print(dao.query(where=' where sex=%s', args=('男',)))
    print(dao.query(where=' where sex=%(sex)s', args=('男',)))