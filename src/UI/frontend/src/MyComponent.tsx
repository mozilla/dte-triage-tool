import React, { useState, useEffect, ReactElement } from 'react';
import { DragDropContext, Droppable, Draggable, DropResult } from 'react-beautiful-dnd';
import { withStreamlitConnection, ComponentProps, Streamlit } from "streamlit-component-lib";

interface Card {
  id: string;
  name: string;
  fields: string[];
  color?: string;
}

interface Column {
  id: string;
  title: string;
  cards: Card[];
}

interface KanbanArgs {
  columns?: Column[];
}

interface KanbanComponentProps extends ComponentProps {
  setComponentValue?: (value: any) => void;
}

function KanbanBoard({ args, setComponentValue }: KanbanComponentProps): ReactElement {
  const { columns: initialColumns } = args;

  const [currentColumns, setCurrentColumns] = useState<Column[]>(
    initialColumns && Array.isArray(initialColumns) ? initialColumns : []
  );

  const onDragEnd = (result: DropResult) => {
    const { source, destination } = result;
    if (!destination) return;

    if (source.droppableId === destination.droppableId && source.index === destination.index) {
        return;
    }

    const newColumns = Array.from(currentColumns);
    const sourceColIndex = newColumns.findIndex((col) => col.id === source.droppableId);
    const destColIndex = newColumns.findIndex((col) => col.id === destination.droppableId);

    const [movedCard] = newColumns[sourceColIndex].cards.splice(source.index, 1);
    newColumns[destColIndex].cards.splice(destination.index, 0, movedCard);

    setCurrentColumns(newColumns);
  };

  useEffect(() => {
    Streamlit.setFrameHeight();
    Streamlit.setComponentValue({ columns: currentColumns });
  }, [currentColumns]);

  return (
    <div style={{ width: '100%' }}>
      <DragDropContext onDragEnd={onDragEnd}>
        <div style={{ display: 'flex', gap: '20px', width: '100%', overflowX: 'auto' }}>
          {currentColumns.map((col) => (
            <Droppable droppableId={col.id} key={col.id}>
              {(provided) => (
                <div
                  ref={provided.innerRef}
                  {...provided.droppableProps}
                  style={{
                    background: '#FAFAFA',
                    padding: '10px',
                    borderRadius: '8px',
                    width: '300px',
                    minHeight: '250px',
                    boxSizing: 'border-box',
                  }}
                >
                  <h3>{col.title}</h3>
                  {col.cards.map((card, cardIndex) => (
                    <Draggable key={card.id} draggableId={card.id} index={cardIndex}>
                      {(provided) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          style={{
                            userSelect: 'none',
                            padding: '8px',
                            margin: '0 0 8px 0',
                            borderRadius: '4px',
                            background: '#fff',
                            border: `2px solid ${card.color || '#000'}`,
                            ...provided.draggableProps.style,
                          }}
                        >
                          <strong>{card.name}</strong>
                          {card.fields?.map((field, i) => (
                            <div key={i}>{field}</div>
                          ))}
                        </div>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          ))}
        </div>
      </DragDropContext>
    </div>
  );
}

export default withStreamlitConnection(KanbanBoard);
