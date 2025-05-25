package org.stos.carcassonne.tile.reader;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.stos.carcassonne.tile.reader.type.ActiveFeature;
import org.stos.carcassonne.tile.reader.type.PassiveFeature;
import org.stos.carcassonne.tile.reader.type.TileDefinition;
import org.stos.carcassonne.tile.reader.type.TileDefinition.Port;
import org.stos.carcassonne.tile.reader.type.TileDefinitionException;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatExceptionOfType;
import static org.stos.carcassonne.tile.reader.type.PortType.F;
import static org.stos.carcassonne.tile.reader.type.PortType.R;
import static org.stos.carcassonne.tile.reader.type.TileDefinition.*;

@ExtendWith(SpringExtension.class)
public class TileResourceLoaderTest {

    private TileResourceLoader tileResourceLoader;

    @BeforeEach
    void setUp() {
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.findAndRegisterModules();
        tileResourceLoader = new TileResourceLoader(objectMapper);
    }

    @Test
    void loads_a_correct_tile() {
        Optional<TileDefinition> tileDefinition = tileResourceLoader.load("test_data/correct_tile.json");

        UUID tileId = UUID.fromString("c7c03a8a-196b-11f0-a65c-331b8482755b");
        TileDefinition expected = new TileDefinition(
                tileId,
                1,
                LocalDate.parse("2025-04-27"),
                "a test json",
                "ABBEY_AND_MAYOR",
                List.of(ActiveFeature.MONASTARY),
                List.of(PassiveFeature.VINEYARD),
                4,
                List.of(
                        new Port(CompositeId.of(tileId, 1), F, List.of(12)),
                        new Port(CompositeId.of(tileId,2), R, List.of(8, 11)),
                        new Port(CompositeId.of(tileId,3), F, List.of(7, 5)),
                        new Port(CompositeId.of(tileId,5), F, List.of(3, 7)),
                        new Port(CompositeId.of(tileId,7), F, List.of(3, 5)),
                        new Port(CompositeId.of(tileId,8), R, List.of(11, 2)),
                        new Port(CompositeId.of(tileId,9), F, List.of(10)),
                        new Port(CompositeId.of(tileId,10), F, List.of(9)),
                        new Port(CompositeId.of(tileId,11), R, List.of(8, 2)),
                        new Port(CompositeId.of(tileId,12), F, List.of(1))
                ));

        assertThat(tileDefinition.orElseThrow()).isEqualTo(expected);
    }

}