package games.action;

import common.GamePanel;
import java.awt.*;
import java.awt.event.KeyEvent;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * ACTION -- "Overload"
 *
 * Your energy bar isn't health, it's fuel. Getting hit by an enemy REFUELS
 * you -- but if you're already near full when you get hit, you overload
 * and it's game over. Pulse attacks (SPACE) clear enemies safely but cost
 * energy, so running low forces you back into the exact risk you're trying
 * to avoid: needing a "safe" hit to keep moving.
 */
public class OverloadGame extends GamePanel {

    private static final int FPS = 60;
    private static final double OVERLOAD_THRESHOLD = 95;
    private static final double PULSE_COST = 22;
    private static final double PULSE_RADIUS = 120;
    private static final double HIT_REFUEL = 26;

    private final Random rnd = new Random();

    private double px, py;
    private double energy = 45;
    private int invulnFrames = 0;
    private int pulseCooldown = 0;
    private int pulseFxFrames = 0;

    private final List<double[]> enemies = new ArrayList<>(); // x, y, speed
    private int spawnTimer = 0;
    private int spawnInterval = 90;
    private double enemySpeedBase = 1.0;

    private int score = 0;
    private int frameCount = 0;

    public OverloadGame(GameOverListener listener) {
        super("Overload", FPS, listener);
        px = 380;
        py = 320;
    }

    @Override
    protected void update() {
        frameCount++;

        boolean moving = false;
        double speed = 3.4;
        if (pressedKeys.contains(KeyEvent.VK_LEFT) || pressedKeys.contains(KeyEvent.VK_A)) { px -= speed; moving = true; }
        if (pressedKeys.contains(KeyEvent.VK_RIGHT) || pressedKeys.contains(KeyEvent.VK_D)) { px += speed; moving = true; }
        if (pressedKeys.contains(KeyEvent.VK_UP) || pressedKeys.contains(KeyEvent.VK_W)) { py -= speed; moving = true; }
        if (pressedKeys.contains(KeyEvent.VK_DOWN) || pressedKeys.contains(KeyEvent.VK_S)) { py += speed; moving = true; }
        px = Math.max(16, Math.min(getWidth() - 16, px));
        py = Math.max(50, Math.min(getHeight() - 16, py));

        energy += moving ? -0.12 : 0.10;
        energy = Math.max(0, Math.min(100, energy));

        if (invulnFrames > 0) invulnFrames--;
        if (pulseCooldown > 0) pulseCooldown--;
        if (pulseFxFrames > 0) pulseFxFrames--;

        if (pressedKeys.contains(KeyEvent.VK_SPACE) && pulseCooldown == 0 && energy >= PULSE_COST) {
            energy -= PULSE_COST;
            pulseCooldown = 26;
            pulseFxFrames = 14;
            enemies.removeIf(en -> {
                double d = Math.hypot(en[0] - px, en[1] - py);
                if (d <= PULSE_RADIUS) {
                    score += 10;
                    return true;
                }
                return false;
            });
        }

        spawnTimer++;
        if (spawnTimer >= spawnInterval) {
            spawnTimer = 0;
            spawnEnemy();
            spawnInterval = Math.max(28, spawnInterval - 1);
        }
        enemySpeedBase = 1.0 + frameCount / 3600.0;

        for (int i = enemies.size() - 1; i >= 0; i--) {
            double[] en = enemies.get(i);
            double dx = px - en[0], dy = py - en[1];
            double d = Math.hypot(dx, dy);
            if (d > 0.01) {
                en[0] += dx / d * en[2];
                en[1] += dy / d * en[2];
            }
            if (d < 20 && invulnFrames == 0) {
                if (energy >= OVERLOAD_THRESHOLD) {
                    endGame(score);
                    return;
                }
                energy = Math.min(100, energy + HIT_REFUEL);
                invulnFrames = 55;
                score += 5;
                enemies.remove(i);
            }
        }

        if (frameCount % FPS == 0) score += 1;
    }

    private void spawnEnemy() {
        int side = rnd.nextInt(4);
        double x, y;
        switch (side) {
            case 0 -> { x = 0; y = rnd.nextDouble() * getHeight(); }
            case 1 -> { x = getWidth(); y = rnd.nextDouble() * getHeight(); }
            case 2 -> { x = rnd.nextDouble() * getWidth(); y = 50; }
            default -> { x = rnd.nextDouble() * getWidth(); y = getHeight(); }
        }
        double speed = enemySpeedBase * (0.9 + rnd.nextDouble() * 0.5);
        enemies.add(new double[]{x, y, speed});
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        g2.setColor(new Color(20, 20, 28));
        g2.fillRect(0, 0, getWidth(), getHeight());

        drawHud(g2);

        if (pulseFxFrames > 0) {
            float t = pulseFxFrames / 14f;
            g2.setColor(new Color(120, 200, 255, (int) (120 * t)));
            int r = (int) (PULSE_RADIUS * (1 - t) + 20);
            g2.drawOval((int) px - r, (int) py - r, r * 2, r * 2);
        }

        for (double[] en : enemies) {
            g2.setColor(new Color(255, 90, 90));
            g2.fillOval((int) en[0] - 9, (int) en[1] - 9, 18, 18);
        }

        Color playerColor = invulnFrames > 0 && invulnFrames % 10 < 5
                ? new Color(255, 255, 255)
                : energyColor();
        g2.setColor(playerColor);
        g2.fillOval((int) px - 12, (int) py - 12, 24, 24);

        g2.setColor(Color.WHITE);
        g2.setFont(new Font("Monospaced", Font.BOLD, 16));
        g2.drawString("Score: " + score, 16, getHeight() - 16);
    }

    private Color energyColor() {
        if (energy >= OVERLOAD_THRESHOLD) return new Color(255, 60, 60);
        if (energy >= 70) return new Color(255, 170, 60);
        return new Color(90, 220, 140);
    }

    private void drawHud(Graphics2D g2) {
        g2.setColor(Color.WHITE);
        g2.setFont(new Font("SansSerif", Font.BOLD, 14));
        g2.drawString("WASD / arrows to move  ·  SPACE = pulse (costs energy)", 16, 22);
        g2.setFont(new Font("SansSerif", Font.PLAIN, 12));
        g2.setColor(new Color(170, 170, 185));
        g2.drawString("Getting hit refuels you -- unless you're already almost full.", 16, 38);

        int barW = getWidth() - 32, barH = 14, barX = 16, barY = 46;
        g2.setColor(new Color(40, 40, 50));
        g2.fillRect(barX, barY, barW, barH);
        g2.setColor(energyColor());
        g2.fillRect(barX, barY, (int) (barW * energy / 100), barH);
        g2.setColor(new Color(255, 255, 255, 160));
        int overloadX = barX + (int) (barW * OVERLOAD_THRESHOLD / 100);
        g2.drawLine(overloadX, barY - 2, overloadX, barY + barH + 2);
    }
}
