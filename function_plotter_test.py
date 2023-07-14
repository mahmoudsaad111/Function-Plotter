import pytest
from function_plotter import MainWindow


@pytest.fixture
def main_window(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    return window

#test if inputs valid so no error
def test_valid_input(main_window):
        main_window.functionInput.setText("10*x")
        main_window.minValueInput.setText("1")
        main_window.maxValueInput.setText("10")
        main_window.plotButton.click()
        assert main_window.errorMessageBox.isHidden() == True
        

def test_empty_inputs(main_window):
        main_window.plotButton.click()
        assert main_window.errorMessageBox.isHidden() == False
        
def test_invalid_function(main_window):
        main_window.functionInput.setText("xy")
        main_window.minValueInput.setText("1")
        main_window.maxValueInput.setText("10")
        main_window.plotButton.click()
        assert main_window.errorMessageBox.isHidden() == False

#tes if user try to replace ^ by ** then  it is error as we support ^ instead of **
def test_invalid_function(main_window):
        main_window.functionInput.setText("x**2")
        main_window.minValueInput.setText("1")
        main_window.maxValueInput.setText("10")
        main_window.plotButton.click()
        assert main_window.errorMessageBox.isHidden() == False
        
def test_invalid_minValue(main_window):
        main_window.functionInput.setText("10*x")
        main_window.minValueInput.setText("h")
        main_window.maxValueInput.setText("10")
        main_window.plotButton.click()
        assert main_window.errorMessageBox.isHidden() == False
    

def test_invalid_maxValue(main_window):
        main_window.functionInput.setText("10*x")
        main_window.minValueInput.setText("1")
        main_window.maxValueInput.setText("msd")
        main_window.plotButton.click()
        assert main_window.errorMessageBox.isHidden() == False
        
# test if minValue smaller than maxValue
def test_maxValue_minVAlue(main_window):
        main_window.functionInput.setText("10*x")
        main_window.minValueInput.setText("10")
        main_window.maxValueInput.setText("1")
        main_window.plotButton.click()
        assert main_window.errorMessageBox.isHidden() == False

#test if function enterd is constant function
def test_const_function(main_window):
        main_window.functionInput.setText("10")
        main_window.minValueInput.setText("1")
        main_window.maxValueInput.setText("10")
        main_window.plotButton.click()
        assert main_window.errorMessageBox.isHidden() == True

#test clear button
def test_clear_button(main_window, qtbot):
    main_window.functionInput.setText("x")
    main_window.minValueInput.setText("0")
    main_window.maxValueInput.setText("10")
    main_window.plotButton.click()
    main_window.clearButton.click()
    
    canvas = main_window.canvas
    ax = canvas.figure.axes[0]

    assert main_window.functionInput.text() == ""
    assert main_window.minValueInput.text() == ""
    assert main_window.maxValueInput.text() == ""
    assert ax.get_lines() == []