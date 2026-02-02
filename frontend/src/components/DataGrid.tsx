import React from "react";

interface Column<T> {
  header: string;
  accessor: (row: T) => React.ReactNode;
}

interface DataGridProps<T> {
  columns: Column<T>[];
  rows: T[];
}

const DataGrid = <T,>({ columns, rows }: DataGridProps<T>) => {
  return (
    <table className="data-grid">
      <thead>
        <tr>
          {columns.map((column, idx) => (
            <th key={idx}>{column.header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row, rowIdx) => (
          <tr key={rowIdx}>
            {columns.map((column, colIdx) => (
              <td key={colIdx}>{column.accessor(row)}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default DataGrid;
