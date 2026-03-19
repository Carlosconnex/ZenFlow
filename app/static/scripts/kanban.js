(() => {
  const board = document.getElementById('kanban-board');
  if (!board) return;
  const boardId = board.dataset.boardId;
  if (!boardId) return;

  let draggingCard = null;

  const dropzones = Array.from(document.querySelectorAll('.k-dropzone'));
  const cardSelector = '.k-card';

  const statusConfig = {
    todo: { text: 'Start', href: (id) => `/boards/${boardId}/move/${id}/doing`, danger: false },
    doing: { text: 'Done', href: (id) => `/boards/${boardId}/move/${id}/done`, danger: false },
    done: { text: 'Clear', href: (id) => `/boards/${boardId}/delete/${id}`, danger: true },
  };

  const updateColumnCounts = () => {
    const columns = document.querySelectorAll('.k-column');
    columns.forEach((column) => {
      const count = column.querySelectorAll(cardSelector).length;
      const pill = column.querySelector('.u-pill');
      if (pill) pill.textContent = String(count);
    });
  };

  const persistMove = async (taskId, newStatus) => {
    const response = await fetch(`/api/boards/${boardId}/tasks/${taskId}/move`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ new_status: newStatus }),
    });

    if (!response.ok) {
      throw new Error('Task move failed');
    }

    return response.json();
  };

  const applyCardState = (card, status) => {
    const taskId = card.dataset.taskId;
    const config = statusConfig[status];
    if (!taskId || !config) return;

    card.classList.remove('k-card-active', 'k-card-done');
    if (status === 'doing') card.classList.add('k-card-active');
    if (status === 'done') card.classList.add('k-card-done');

    const actionLink = card.querySelector('[data-role="workflow-action"]');
    if (!actionLink) return;

    actionLink.textContent = config.text;
    actionLink.href = config.href(taskId);
    actionLink.classList.toggle('u-card-link-danger', config.danger);
  };

  const createModal = document.getElementById('create-task-modal');
  const editModal = document.getElementById('edit-task-modal');
  const editForm = document.getElementById('edit-task-form');
  const editTitle = document.getElementById('edit-title');
  const editDescription = document.getElementById('edit-description');
  const editComplexity = document.getElementById('edit-complexity');

  const openModal = (modal) => {
    if (!modal) return;
    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
  };

  const closeModal = (modal) => {
    if (!modal) return;
    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden', 'true');
  };

  const resetDropStates = () => {
    dropzones.forEach((zone) => zone.classList.remove('is-over'));
  };

  document.addEventListener('dragstart', (event) => {
    const card = event.target.closest(cardSelector);
    if (!card) return;

    draggingCard = card;
    card.classList.add('is-dragging');
    event.dataTransfer.effectAllowed = 'move';
    event.dataTransfer.setData('text/plain', card.dataset.taskId || '');
  });

  document.addEventListener('dragend', () => {
    if (draggingCard) {
      draggingCard.classList.remove('is-dragging');
    }
    draggingCard = null;
    resetDropStates();
  });

  dropzones.forEach((zone) => {
    zone.addEventListener('dragover', (event) => {
      event.preventDefault();
      zone.classList.add('is-over');
    });

    zone.addEventListener('dragleave', () => {
      zone.classList.remove('is-over');
    });

    zone.addEventListener('drop', async (event) => {
      event.preventDefault();
      zone.classList.remove('is-over');

      if (!draggingCard) return;

      const sourceZone = draggingCard.closest('.k-dropzone');
      const sourceStatus = sourceZone?.dataset.status;
      const targetStatus = zone.dataset.status;
      const taskId = draggingCard.dataset.taskId;

      if (!taskId || !targetStatus || targetStatus === sourceStatus) return;

      zone.appendChild(draggingCard);
      applyCardState(draggingCard, targetStatus);
      updateColumnCounts();

      try {
        const payload = await persistMove(taskId, targetStatus);
        if (payload?.new_status) {
          applyCardState(draggingCard, payload.new_status);
        }
      } catch {
        // Revert UI to keep frontend and backend in sync on failure.
        if (sourceZone) {
          sourceZone.appendChild(draggingCard);
          if (sourceStatus) {
            applyCardState(draggingCard, sourceStatus);
          }
        }
        updateColumnCounts();
      }
    });
  });

  document.querySelector('[data-open-create-modal]')?.addEventListener('click', () => {
    openModal(createModal);
  });

  document.querySelectorAll('[data-open-edit-modal]').forEach((button) => {
    button.addEventListener('click', () => {
      const taskId = button.dataset.taskId;
      if (!taskId || !editForm || !editTitle || !editDescription || !editComplexity) return;

      editForm.action = `/boards/${boardId}/tasks/${taskId}/edit`;
      editTitle.value = button.dataset.taskTitle || '';
      editDescription.value = button.dataset.taskDescription || '';

      const energy = button.dataset.taskEnergy || '2';
      editComplexity.value = energy === '1' ? 'low' : energy === '3' ? 'high' : 'medium';
      openModal(editModal);
    });
  });

  document.querySelectorAll('[data-close-modal]').forEach((button) => {
    button.addEventListener('click', () => {
      closeModal(createModal);
      closeModal(editModal);
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    closeModal(createModal);
    closeModal(editModal);
  });
})();
