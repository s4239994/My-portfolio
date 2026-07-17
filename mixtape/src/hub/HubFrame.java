package hub;

import common.GamePanel;
import common.HighScores;
import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;
import java.util.List;

public class HubFrame extends JFrame implements GamePanel.GameOverListener {

    private static final String MENU_CARD = "MENU";
    private final CardLayout cardLayout = new CardLayout();
    private final JPanel content = new JPanel(cardLayout);
    private final HighScores scores = new HighScores();
    private final List<GameEntry> entries = new ArrayList<>();
    private GamePanel activeGame;

    public HubFrame(List<GameEntry> entries) {
        super("Mixtape");
        this.entries.addAll(entries);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(760, 640);
        setMinimumSize(new Dimension(600, 500));
        setLocationRelativeTo(null);

        content.add(buildMenu(), MENU_CARD);
        setContentPane(content);
    }

    private MenuPanel buildMenu() {
        return new MenuPanel(entries, scores, this::launchGame);
    }

    private void launchGame(GameEntry entry) {
        activeGame = entry.launcher.apply(this);
        content.add(activeGame, entry.title);
        cardLayout.show(content, entry.title);
        activeGame.startGame();
    }

    @Override
    public void onGameOver(int score, String gameName) {
        boolean newBest = scores.submit(gameName, score);
        String message = newBest
                ? "New high score: " + score + "!"
                : "Score: " + score + "  (best: " + scores.get(gameName) + ")";
        SwingUtilities.invokeLater(() -> {
            JOptionPane.showMessageDialog(this, message, gameName + " -- Game Over", JOptionPane.PLAIN_MESSAGE);
            activeGame = null;
            refreshMenuAndShow();
        });
    }

    private void refreshMenuAndShow() {
        content.removeAll();
        content.add(buildMenu(), MENU_CARD);
        cardLayout.show(content, MENU_CARD);
        content.revalidate();
        content.repaint();
    }
}
