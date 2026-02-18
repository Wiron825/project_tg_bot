from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, text
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime, date, time, timedelta


Base = declarative_base()
engine = create_engine(
    "sqlite:///project_tg_bot/bd/mybd.sqlite3",
    echo=True
)

class User(Base):
    __tablename__ = "changes"
    time_street = Column(String, primary_key=True)
    streets_better = Column(String)
    streets_worse = Column(String)
    count_peple = Column(Integer)
    count_aktive_peple = Column(Integer)

Base.metadata.create_all(engine)


def delete():
    with engine.begin()as conn:
        conn.execute(text("DELETE FROM changes"))

def name_time():
    with engine.begin()as conn:
        data = conn.execute(text("SELECT time_street FROM changes"))
        data = [i for row in data for i in row]
    return data

def new_changes(streets_better='', streets_worse='', count_peple=0, count_aktive_peple=0):
    if date.today().strftime("%Y-%m-%d") not in name_time:
        with Session(engine) as session:
            data_user = date.today().strftime("%Y-%m-%d")
            new_user = User(time_street=data_user, streets_better=streets_better, streets_worse=streets_worse, count_peple=count_peple, count_aktive_peple=count_aktive_peple)
            session.add(new_user)
            session.commit()

def old_day(data=date.today().strftime("%Y-%m-%d")):
    try:
        data = list(map(int, data.split('-')))
        if len(data) != 3:
            return 'дата не верна'
        dicts = {(1, 2, 4, 6, 8, 10, 11): 30}
        data[2] = data[2] - 1 if data[2] - 1 > 0 else -1
        if data[2] < 0:
            for i in dicts:
                if data[1] in i:
                    if data[1] - 1 <= 0:
                        data[0] -= 1
                        data[1] = 12
                        data[2] = 31
                    else:
                        data[1] -= 1
                        data[2] = 31
                elif data[1] == 3:
                    data[1] -= 1
                    data[2] = 28
                else:
                    data[1] -= 1
                    data[2] = 30  
        data[0] = f'0{data[0]}' if data[0] < 10 else str(data[0])
        data[1] = f'0{data[1]}' if data[1] < 10 else str(data[1])
        data[2] = f'0{data[2]}' if data[2] < 10 else str(data[2])
        data = '-'.join(data)
        print(data)
        return data
    except Exception as _e:
        print(_e)
        return _e

# old_count_peple('2026-01-01')
# old_count_peple('2026-03-01')
# old_count_peple('2026-11-01')
# old_count_peple('2026-01-11')
# old_count_peple()