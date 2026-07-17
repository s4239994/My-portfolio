package common;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.HashSet;
import java.util.Set;

/**
 * Shared base for every mini-game: owns the Swing Timer game loop,
 * keyboard/mouse input tracking, and the game-over callback. Each game
 * only has to implement update() and paint logic.
 */
public abstract class GamePanel extends JPanel implements ActionListener {

    public interface GameOverListener {
        void onGameOver(int score, String gameName);
    }

    protected final Set<Integer> pressedKeys = new HashSet<>();
    protected int mouseX, mouseY;
    protected boolean mouseDown;
    protected boolean mouseClicked;
    protected int clickX, clickY;

    protected final Timer timer;
    protected boolean running = false;
    protected final GameOverListener listener;
    protected final String gameName;

    public GamePanel(String gameName, int fps, GameOverListener listener) {
        this.gameName = gameName;
        this.listener = listener;
        setFocusable(true);
        setBackground(Color.BLACK);

        addKeyListener(new KeyAdapter() {
            @Override public void keyPressed(KeyEvent e) { pressedKeys.add(e.getKeyCode()); }
            @Override public void keyReleased(KeyEvent e) { pressedKeys.remove(e.getKeyCode()); }
        });
        addMouseListener(new MouseAdapter() {
            @Override public void mousePressed(MouseEvent e) { mouseDown = true; }
            @Override public void mouseReleased(MouseEvent e) { mouseDown = false; }
            @Override public void mouseClicked(MouseEvent e) {
                mouseClicked = true;
                clickX = e.getX();
                clickY = e.getY();
            }
        });
        addMouseMotionListener(new MouseMotionAdapter() {
            @Override public void mouseMoved(MouseEvent e) { mouseX = e.getX(); mouseY = e.getY(); }
            @Override public void mouseDragged(MouseEvent e) { mouseX = e.getX(); mouseY = e.getY(); }
        });

        timer = new Timer(1000 / fps, this);
    }

    public void startGame() {
        running = true;
        timer.start();
        requestFocusInWindow();
    }

    public void stopGame() {
        running = false;
        timer.stop();
    }

    @Override
    public final void actionPerformed(ActionEvent e) {
        if (!running) return;
        update();
        mouseClicked = false;
        repaint();
    }

    protected void endGame(int score) {
        stopGame();
        if (listener != null) listener.onGameOver(score, gameName);
    }

    protected abstract void update();
}
