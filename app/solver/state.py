import arcade

class State:

  ACTION_LEFT = 0
  ACTION_RIGHT = 1
  ACTION_UP = 2
  ACTION_DOWN = 3

  def __init__(self, width, height):
    self.width = width
    self.height = height

    self.indexRow = -1
    self.indexCol = -1
    self.indexMovingRow = -1
    self.indexMovingCol = -1
    self.offsetX = 0
    self.offsetY = 0

    self.animationTime = 2
    self.accumulatedTime = 0

    self.solution = []
    self.solutionIndex = 0

    self.state = [
      [2, 1, 3],
      [5, 4, 6],
      [7, 8, 0]
    ]

  def render(self):
    for j in range(3):
      for i in range(3):
        if self.state[i][j] != 0:
          if i == self.indexMovingRow and j == self.indexMovingCol:
            arcade.draw_lrtb_rectangle_outline(
              (j + 0) * self.width / 3 + 5 + self.offsetX,
              (j + 1) * self.width / 3 - 5 + self.offsetX,
              self.height - (i + 0) * self.height / 3 - 5 + self.offsetY,
              self.height - (i + 1) * self.height / 3 + 5 + self.offsetY,
              arcade.color.BLACK)

            arcade.draw_text(
              str(self.state[i][j]),
              j * self.width / 3 + self.width / 3 / 2 + self.offsetX,
              self.height - i * self.height / 3 - self.height / 3 / 2 + self.offsetY,
              arcade.color.BLACK,
              64,
              align="center",
              anchor_x="center",
              anchor_y="center")
          else:
            arcade.draw_lrtb_rectangle_outline(
              (j + 0) * self.width / 3 + 5,
              (j + 1) * self.width / 3 - 5,
              self.height - (i + 0) * self.height / 3 - 5,
              self.height - (i + 1) * self.height / 3 + 5,
              arcade.color.BLACK)

            arcade.draw_text(
              str(self.state[i][j]),
              j * self.width / 3 + self.width / 3 / 2,
              self.height - i * self.height / 3 - self.height / 3 / 2,
              arcade.color.BLACK,
              64,
              align="center",
              anchor_x="center",
              anchor_y="center")

  def update(self, elapsed_time):
    if self.solutionIndex >= len(self.solution):
      return

    self.accumulatedTime += elapsed_time
    currentAction = self.solution[self.solutionIndex]

    if self.accumulatedTime > self.animationTime:
      self.accumulatedTime = 0

      if currentAction == self.ACTION_LEFT:
        self.state[self.indexRow][self.indexCol-1], self.state[self.indexRow][self.indexCol] = self.state[self.indexRow][self.indexCol], self.state[self.indexRow][self.indexCol-1]
        self.indexCol -= 1
      elif currentAction == self.ACTION_RIGHT:
        self.state[self.indexRow][self.indexCol+1], self.state[self.indexRow][self.indexCol] = self.state[self.indexRow][self.indexCol], self.state[self.indexRow][self.indexCol+1]
        self.indexCol += 1
      elif currentAction == self.ACTION_UP:
        self.state[self.indexRow-1][self.indexCol], self.state[self.indexRow][self.indexCol] = self.state[self.indexRow][self.indexCol], self.state[self.indexRow-1][self.indexCol]
        self.indexRow -= 1
      elif currentAction == self.ACTION_DOWN:
        self.state[self.indexRow+1][self.indexCol], self.state[self.indexRow][self.indexCol] = self.state[self.indexRow][self.indexCol], self.state[self.indexRow+1][self.indexCol]
        self.indexRow += 1

      self.solutionIndex += 1
      if self.solutionIndex >= len(self.solution):
        self.solutionIndex = len(self.solution)
        return

    if currentAction == self.ACTION_LEFT:
      self.offsetX = +self.accumulatedTime * self.width / 3 / self.animationTime
      self.indexMovingRow = self.indexRow
      self.indexMovingCol = self.indexCol - 1
    elif currentAction == self.ACTION_RIGHT:
      self.offsetX = -self.accumulatedTime * self.width / 3 / self.animationTime
      self.indexMovingRow = self.indexRow
      self.indexMovingCol = self.indexCol + 1
    elif currentAction == self.ACTION_UP:
      self.offsetY = -self.accumulatedTime * self.height / 3 / self.animationTime
      self.indexMovingRow = self.indexRow - 1
      self.indexMovingCol = self.indexCol
    elif currentAction == self.ACTION_DOWN:
      self.offsetY = self.accumulatedTime * self.height / 3 / self.animationTime
      self.indexMovingRow = self.indexRow + 1
      self.indexMovingCol = self.indexCol

  def solve(self):
    self.solution = self._solve()
    print(self.solution)
    for i in range(3):
      for j in range(3):
        if self.state[i][j] == 0:
          self.indexRow = i
          self.indexCol = j
          return

  def isGoal(self):
    return self._isGoal(self.state)

  def _solve(self):
    if self.isGoal():
      return []

    ci = -1
    cj = -1
    for i in range(3):
      for j in range(3):
        if self.state[i][j] == 0:
          ci = i
          cj = j

    visited = {}
    stack = [{
      'state': self.state,
      'actions': [],
      'i': ci,
      'j': cj
    }]

    actions = [
      self.ACTION_LEFT,
      self.ACTION_RIGHT,
      self.ACTION_UP,
      self.ACTION_DOWN
    ]

    while len(stack) > 0:
      node = stack.pop(0)
      state = node['state']
      acts = node['actions']
      ci = node['i']
      cj = node['j']

      if self._isGoal(state) == True:
        return acts

      for action in actions:
        ti = -1
        tj = -1
        newActs = []
        newState = []

        for i in state:
          newState.append(i.copy())

        if action == self.ACTION_LEFT and cj > 0:
          newState[ci][cj], newState[ci][cj-1] = newState[ci][cj-1], newState[ci][cj]
          newActs = acts.copy()
          newActs.append(self.ACTION_LEFT)
          ti = ci
          tj = cj - 1
        elif action == self.ACTION_RIGHT and cj < 2:
          newState[ci][cj], newState[ci][cj+1] = newState[ci][cj+1], newState[ci][cj]
          newActs = acts.copy()
          newActs.append(self.ACTION_RIGHT)
          ti = ci
          tj = cj + 1
        elif action == self.ACTION_UP and ci > 0:
          newState[ci][cj], newState[ci-1][cj] = newState[ci-1][cj], newState[ci][cj]
          newActs = acts.copy()
          newActs.append(self.ACTION_UP)
          ti = ci - 1
          tj = cj
        elif action == self.ACTION_DOWN and ci < 2:
          newState[ci][cj], newState[ci+1][cj] = newState[ci+1][cj], newState[ci][cj]
          newActs = acts.copy()
          newActs.append(self.ACTION_DOWN)
          ti = ci + 1
          tj = cj
        else:
          continue

        hash = []
        for i in newState:
          for j in i:
            hash.append(str(j))

        stamp = ','.join(hash)
        if visited.get(stamp) == None:
          visited[stamp] = True
        else:
          continue

        stack.append({
          'state': newState,
          'actions': newActs,
          'i': ti,
          'j': tj
        })
        # print(len(stack))

    return []

  def _isGoal(self, state):
    counter = 1
    for i in range(3):
      for j in range(3):
        if counter == 9 and state[i][j] != 0:
          return False
        elif counter != 9 and state[i][j] != counter:
          return False
        counter += 1
    return True