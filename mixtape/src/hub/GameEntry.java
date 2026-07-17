package hub;

import common.GamePanel;
import java.awt.Color;
import java.util.function.Function;

/** Describes one genre's mini-game for the hub menu. */
public class GameEntry {
    public final String genre;
    public final String title;
    public final String tagline;
    public final Color accent;
    public final Function<GamePanel.GameOverListener, GamePanel> launcher;

    public GameEntry(String genre, String title, String tagline, Color accent,
                      Function<GamePanel.GameOverListener, GamePanel> launcher) {
        this.genre = genre;
        this.title = title;
        this.tagline = tagline;
        this.accent = accent;
        this.launcher = launcher;
    }
}
