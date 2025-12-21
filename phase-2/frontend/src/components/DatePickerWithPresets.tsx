"use client";

import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { addDays, addWeeks, endOfMonth } from "date-fns";

interface DatePickerWithPresetsProps {
  selected: Date | null;
  onChange: (date: Date | null) => void;
  minDate?: Date;
  className?: string;
}

export default function DatePickerWithPresets({
  selected,
  onChange,
  minDate = new Date(),
  className = "",
}: DatePickerWithPresetsProps) {
  const [showCalendar, setShowCalendar] = useState(false);

  const presets = [
    { label: "Complete in 1 day", getValue: () => addDays(new Date(), 1) },
    { label: "Complete in 2 days", getValue: () => addDays(new Date(), 2) },
    {
      label: "Complete in a week",
      getValue: () => addWeeks(new Date(), 1),
    },
    {
      label: "Complete in 2 weeks",
      getValue: () => addWeeks(new Date(), 2),
    },
    { label: "End of month", getValue: () => endOfMonth(new Date()) },
  ];

  const handlePresetClick = (getValue: () => Date) => {
    const date = getValue();
    onChange(date);
    setShowCalendar(false);
  };

  const handleCustomDateChange = (date: Date | null) => {
    onChange(date);
    setShowCalendar(false);
  };

  const formatSelectedDate = (date: Date | null) => {
    if (!date) return "Select completion date";
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  return (
    <div className={`relative ${className}`}>
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Target Completion Date{" "}
          {selected && (
            <span className="text-xs text-gray-500 dark:text-gray-400">
              (Currently set)
            </span>
          )}
        </label>

        {selected && (
          <div className="flex items-center gap-2 px-3 py-2 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-md">
            <svg
              className="w-4 h-4 text-blue-600 dark:text-blue-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
            <span className="text-sm font-medium text-blue-700 dark:text-blue-300">
              Due: {formatSelectedDate(selected)}
            </span>
          </div>
        )}

        <button
          type="button"
          onClick={() => setShowCalendar(!showCalendar)}
          className={`w-full px-4 py-2 text-left border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            selected
              ? "border-blue-300 dark:border-blue-600 bg-blue-50 dark:bg-blue-900/10 text-blue-900 dark:text-blue-100"
              : "border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400"
          } hover:border-blue-500 dark:hover:border-blue-400`}
        >
          {selected ? "Change date" : "Select completion date"}
        </button>

        {showCalendar && (
          <div className="absolute z-50 mt-2 p-4 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-lg">
            <div className="space-y-3">
              <div className="grid grid-cols-1 gap-2">
                {presets.map((preset) => (
                  <button
                    key={preset.label}
                    type="button"
                    onClick={() => handlePresetClick(preset.getValue)}
                    className="px-4 py-2 text-sm text-left bg-gray-100 dark:bg-gray-700 hover:bg-blue-500 hover:text-white dark:hover:bg-blue-600 rounded-md transition-colors"
                  >
                    {preset.label}
                  </button>
                ))}
              </div>

              <div className="border-t border-gray-200 dark:border-gray-700 pt-3">
                <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">
                  Or pick a custom date:
                </p>
                <DatePicker
                  selected={selected}
                  onChange={handleCustomDateChange}
                  minDate={minDate}
                  inline
                  className="w-full"
                />
              </div>

              {selected && (
                <button
                  type="button"
                  onClick={() => {
                    onChange(null);
                    setShowCalendar(false);
                  }}
                  className="w-full px-4 py-2 text-sm bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200 hover:bg-red-200 dark:hover:bg-red-800 rounded-md"
                >
                  Clear Date
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
