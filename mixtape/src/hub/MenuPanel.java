package hub;

import common.HighScores;
import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.List;

public class MenuPanel extends JPanel {

    public interface LaunchListener {
        void onLaunch(GameEntry entry);
    }

    public MenuPanel(List<GameEntry> entries, HighScores scores, LaunchListener launchListener) {
        setLayout(new BorderLayout());
        setBackground(new Color(18, 18, 24));

        JLabel title = new JLabel("MIXTAPE");
        title.setFont(new Font("SansSerif", Font.BOLD, 42));
        title.setForeground(Color.WHITE);
        title.setBorder(BorderFactory.createEmptyBorder(28, 32, 4, 0));

        JLabel subtitle = new JLabel("Pick a genre. Every one plays differently than you expect.");
        subtitle.setFont(new Font("SansSerif", Font.PLAIN, 15));
        subtitle.setForeground(new Color(160, 160, 175));
        subtitle.setBorder(BorderFactory.createEmptyBorder(0, 32, 20, 0));

        JPanel header = new JPanel();
        header.setLayout(new BoxLayout(header, BoxLayout.Y_AXIS));
        header.setBackground(getBackground());
        header.add(title);
        header.add(subtitle);
        add(header, BorderLayout.NORTH);

        JPanel grid = new JPanel(new GridLayout(0, 1, 0, 16));
        grid.setBackground(getBackground());
        grid.setBorder(BorderFactory.createEmptyBorder(0, 32, 32, 32));

        for (GameEntry entry : entries) {
            grid.add(buildCard(entry, scores, launchListener));
        }

        JScrollPane scroll = new JScrollPane(grid);
        scroll.setBorder(null);
        scroll.getVerticalScrollBar().setUnitIncrement(16);
        add(scroll, BorderLayout.CENTER);
    }

    private JPanel buildCard(GameEntry entry, HighScores scores, LaunchListener launchListener) {
        JPanel card = new JPanel(new BorderLayout());
        card.setBackground(new Color(28, 28, 36));
        card.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createMatteBorder(0, 6, 0, 0, entry.accent),
                BorderFactory.createEmptyBorder(16, 20, 16, 20)
        ));
        card.setMaximumSize(new Dimension(Integer.MAX_VALUE, 100));
        card.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));

        JLabel genreLabel = new JLabel(entry.genre.toUpperCase());
        genreLabel.setFont(new Font("SansSerif", Font.BOLD, 12));
        genreLabel.setForeground(entry.accent);

        JLabel titleLabel = new JLabel(entry.title);
        titleLabel.setFont(new Font("SansSerif", Font.BOLD, 22));
        titleLabel.setForeground(Color.WHITE);

        JLabel taglineLabel = new JLabel(entry.tagline);
        taglineLabel.setFont(new Font("SansSerif", Font.PLAIN, 13));
        taglineLabel.setForeground(new Color(170, 170, 185));

        JPanel textPanel = new JPanel();
        textPanel.setLayout(new BoxLayout(textPanel, BoxLayout.Y_AXIS));
        textPanel.setOpaque(false);
        textPanel.add(genreLabel);
        textPanel.add(titleLabel);
        textPanel.add(taglineLabel);
        card.add(textPanel, BorderLayout.CENTER);

        JLabel scoreLabel = new JLabel("BEST  " + scores.get(entry.title));
        scoreLabel.setFont(new Font("Monospaced", Font.BOLD, 14));
        scoreLabel.setForeground(entry.accent);
        card.add(scoreLabel, BorderLayout.EAST);

        card.addMouseListener(new MouseAdapter() {
            @Override public void mouseClicked(MouseEvent e) { launchListener.onLaunch(entry); }
            @Override public void mouseEntered(MouseEvent e) { card.setBackground(new Color(38, 38, 48)); }
            @Override public void mouseExited(MouseEvent e) { card.setBackground(new Color(28, 28, 36)); }
        });

        return card;
    }
}
