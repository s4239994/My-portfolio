package common;

import java.io.*;
import java.nio.file.*;
import java.util.Properties;

/** Simple local high-score storage, one integer per game, in data/highscores.properties. */
public class HighScores {

    private static final Path FILE = Paths.get("data", "highscores.properties");
    private final Properties props = new Properties();

    public HighScores() {
        load();
    }

    private void load() {
        if (Files.exists(FILE)) {
            try (InputStream in = Files.newInputStream(FILE)) {
                props.load(in);
            } catch (IOException ignored) {
            }
        }
    }

    public int get(String gameName) {
        return Integer.parseInt(props.getProperty(gameName, "0"));
    }

    public boolean submit(String gameName, int score) {
        int best = get(gameName);
        if (score <= best) return false;
        props.setProperty(gameName, String.valueOf(score));
        save();
        return true;
    }

    private void save() {
        try {
            Files.createDirectories(FILE.getParent());
            try (OutputStream out = Files.newOutputStream(FILE)) {
                props.store(out, "Mixtape high scores");
            }
        } catch (IOException ignored) {
        }
    }
}
