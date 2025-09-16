import React, { useState, useEffect, ReactElement } from "react";
import {
  DragDropContext,
  Droppable,
  Draggable,
  DropResult,
} from "react-beautiful-dnd";
import {
  withStreamlitConnection,
  ComponentProps,
  Streamlit,
} from "streamlit-component-lib";

interface Card {
  id: string;
  name: string;
  fields: string[];
  color?: string;
}

interface MovedCards {
  [key: string]: [string, string];
}

interface Column {
  id: string;
  title: string;
  cards: Card[];
}

interface KanbanComponentProps extends ComponentProps {
  setComponentValue?: (value: any) => void;
}

function KanbanBoard({ args }: KanbanComponentProps): ReactElement {
  const { columns: initialColumns } = args;

  const [currentColumns, setCurrentColumns] = useState<Column[]>(
    initialColumns && Array.isArray(initialColumns) ? initialColumns : []
  );

  const [movedCards, setMovedCards] = useState<MovedCards[]>([{}]);

  const onDragEnd = (result: DropResult) => {
    const { source, destination } = result;
    if (!destination) return;

    if (
      source.droppableId === destination.droppableId &&
      source.index === destination.index
    ) {
      return;
    }

    const newColumns = Array.from(currentColumns);
    const newMovedCards = Array.from(movedCards).at(0) || {};
    const sourceColIndex = newColumns.findIndex(
      (col) => col.id === source.droppableId
    );
    const destColIndex = newColumns.findIndex(
      (col) => col.id === destination.droppableId
    );

    const [droppedCard] = newColumns[sourceColIndex].cards.splice(
      source.index,
      1
    );
    newColumns[destColIndex].cards.splice(destination.index, 0, droppedCard);

    if (newMovedCards[droppedCard.id]) {
      if (newMovedCards[droppedCard.id][0] === destination.droppableId) {
        delete newMovedCards[droppedCard.id];
      } else {
        newMovedCards[droppedCard.id][1] = destination.droppableId;
      }
    } else {
      newMovedCards[droppedCard.id] = [
        source.droppableId,
        destination.droppableId,
      ];
    }
    setMovedCards([newMovedCards]);
    setCurrentColumns(newColumns);
    console.log([newMovedCards]);
  };

  useEffect(() => {
    Streamlit.setFrameHeight();
    Streamlit.setComponentValue(movedCards);
  }, [movedCards]);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        overflowY: "hidden",
        fontFamily: "sans-serif, sans-serif, monospace",
      }}
    >
      <DragDropContext onDragEnd={onDragEnd}>
        <div
          style={{
            display: "flex",
            gap: "20px",
            width: "100%",
            overflowX: "auto",
          }}
        >
          {currentColumns.map((col) => (
            <Droppable droppableId={col.id} key={col.id}>
              {(provided) => (
                <div
                  ref={provided.innerRef}
                  {...provided.droppableProps}
                  style={{
                    background: "#FAFAFA",
                    padding: "10px",
                    borderRadius: "8px",
                    minWidth: "18em",
                    minHeight: "30em",
                    maxHeight: "35em",
                    boxSizing: "border-box",
                    overflowY: "auto",
                  }}
                >
                  <h3 style={{ textAlign: "center", margin: "0 0 10px 0" }}>
                    {col.title}
                  </h3>
                  {col.cards.map((card, cardIndex) => (
                    <Draggable
                      key={`card-${card.id}`}
                      draggableId={card.id}
                      index={cardIndex}
                      shouldRespectForcePress={true}
                    >
                      {(provided) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          style={{
                            userSelect: "none",
                            padding: "8px",
                            margin: "0 0 8px 0",
                            borderRadius: "4px",
                            background: "#fff",
                            fontFamily: "Inter, system-ui, sans-serif",
                            border: `2px solid ${card.color || "#000"}`,
                            ...provided.draggableProps.style,
                          }}
                        >
                          <strong>{card.name}</strong>
                          {card.fields?.map((field, i) => (
                            <div key={i}>{field}</div>
                          ))}
                          <a
                            target="_blank"
                            rel="noreferrer"
                            href={`https://mozilla.testrail.io/index.php?/cases/view/${card.id}`}
                          >
                            Go to Test Case
                          </a>
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
