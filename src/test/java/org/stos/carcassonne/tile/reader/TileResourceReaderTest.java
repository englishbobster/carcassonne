package org.stos.carcassonne.tile.reader;

import org.junit.jupiter.api.Test;
import org.stos.carcassonne.tile.reader.TileDefinition.Port;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;
import static org.stos.carcassonne.tile.reader.PortType.F;
import static org.stos.carcassonne.tile.reader.PortType.R;

public class TileResourceReaderTest {

    @Test
    void read_a_tile() {
        TileLoader tileLoader = new TileLoader();
        TileDefinition tileDefinition = tileLoader.load();

        TileDefinition expected = new TileDefinition(
                UUID.fromString("c7c03a8a-196b-11f0-a65c-331b8482755b"),
                1,
                LocalDate.parse("2025-04-27"),
                "a test json",
                "ABBEY_AND_MAYOR",
                List.of(ActiveFeature.MONASTARY),
                List.of(PassiveFeature.VINEYARD),
                4,
                List.of(
                        new Port(1, F, List.of(12)),
                        new Port(2, R, List.of(8, 11)),
                        new Port(3, F, List.of(7, 5)),
                        new Port(5, F, List.of(3, 7)),
                        new Port(7, F, List.of(3, 5)),
                        new Port(8, R, List.of(11, 2)),
                        new Port(9, F, List.of(10)),
                        new Port(10, F, List.of(9)),
                        new Port(11, R, List.of(8, 2)),
                        new Port(12, F, List.of(1))
                ));

        assertThat(tileDefinition).isEqualTo(expected);
    }


}