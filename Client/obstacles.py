        # Obstacle Avoidance
        if (driver.getMovement() == 'forward' and rangerF.getDist() < 30) or (driver.getMovement() == 'backward' and rangerB.getDist() < 30):
            # get original direction it was going 
            originalDir = driver.getMovement()
            # stop the vehicle
            driver.stop()
            # determine which way to turn
            turnDir = rangerL.isMax(rangerR)
            originalTurn = 'right'
            if turnDir:
                driver.turnLeft()
                originalTurn = 'left'
                if originalDir == 'forward':
                    while rangerR.getDist() < 50:
                        driver.forward()
                else:
                    while rangerL.getDist() < 50:
                        driver.forward()
            else:
                driver.turnRight()
                if originalDir == 'forward':
                    while rangerL.getDist() < 50:
                        driver.forward()
                else:
                    while rangerR.getDist() < 50:
                        driver.forward()

            # Looking at wrong sensor: obstacleVisible is changed by one of the side rangers
            # Look to make this simpler

            # always go forward since we determined which side had more room 

            if originalTurn == 'right':
                driver.turnLeft()
            else:
                driver.turnRight()

            if originalDir == 'forward':
                driver.forward()
            else:
                driver.backward()
            