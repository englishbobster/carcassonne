package org.stos.carcassonne.tile.reader.type;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

public record TileDefinition(
        UUID tileId,
        int version,
        LocalDate updatedAt,
        String description,
        String expansion,
        List<ActiveFeature> activeFeatures,
        List<PassiveFeature> passiveFeatures,
        int shields,
        List<Port> ports
) {

    public TileDefinition {
        ports = ports.stream()
                .map(port -> new Port(
                        new CompositeId(tileId, port.id().portId),
                        port.type(),
                        port.connections()
                ))
                .toList();
    }


    public record Port(
            @JsonProperty("id")
            CompositeId id,
            @JsonProperty("type")
            PortType type,
            @JsonProperty("connections")
            List<Integer> connections
    ) {

        @JsonCreator(mode = JsonCreator.Mode.PROPERTIES)
        public static Port create( @JsonProperty("id")int id,
                                   @JsonProperty("type") PortType type,
                                   @JsonProperty("connections") List<Integer> connections) {
            return new Port(new CompositeId(null, id), type, connections);
        }
    }

    public record CompositeId(UUID tileId, int portId) {
        public static CompositeId of(UUID tileId, int portId) {
            return new CompositeId(tileId, portId);
        }
    }
}