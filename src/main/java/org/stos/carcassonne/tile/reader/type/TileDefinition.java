package org.stos.carcassonne.tile.reader.type;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

    public record TileDefinition(
            UUID id,
            int version,
            LocalDate updatedAt,
            String description,
            String expansion,
            List<ActiveFeature> activeFeatures,
            List<PassiveFeature> passiveFeatures,
            int shields,
            List<Port> ports
    ) {
        public record Port(
                int id,
                PortType type,
                List<Integer> connections
        ) { }
    }