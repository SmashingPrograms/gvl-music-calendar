import React, { useState } from "react";
import Calendar, { CalendarTileProperties } from "react-calendar";
import "react-calendar/dist/Calendar.css";
import './CalendarStyles.css';

interface Props {}

const MyCalendar: React.FC<Props> = () => {
  const [date, setDate] = useState<Date>(new Date());

  const tileDisabledHandler = ({ date, view }: CalendarTileProperties) => {
    if (view === "month") {
      return date.getDay() === 0 || date.getDay() === 6;
    }
  };

  const tileClassNameHandler = ({
    date,
    view
  }: CalendarTileProperties): string => {
    if (view === "month") {
      if (date.getDate() === 14) {
        return "special-date";
      }
    }
    return "";
  };

  const onChangeHandler = (date: Date | Date[]) => {
    setDate(date as Date);
  };

  return (
    <div>
      <Calendar
        className="weekdays"
        value={date}
        onChange={onChangeHandler}
        tileDisabled={tileDisabledHandler}
        tileClassName={tileClassNameHandler}
      />
    </div>
  );
};

export default MyCalendar;