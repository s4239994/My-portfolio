import hub.GameEntry;
import hub.HubFrame;
import games.action.OverloadGame;

import javax.swing.*;
import java.awt.Color;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<GameEntry> entries = List.of(
                new GameEntry(
                        "Action",
                        "Overload",
                        "Getting hit refuels you. Getting hit while full ends you.",
                        new Color(255, 110, 90),
                        OverloadGame::new
                )
        );

        SwingUtilities.invokeLater(() -> {
            HubFrame frame = new HubFrame(entries);
            frame.setVisible(true);
        });
    }
}
