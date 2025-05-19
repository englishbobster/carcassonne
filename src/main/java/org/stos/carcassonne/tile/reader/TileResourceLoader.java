package org.stos.carcassonne.tile.reader;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;
import org.stos.carcassonne.tile.reader.type.TileDefinition;
import org.stos.carcassonne.tile.reader.type.TileDefinitionException;

import java.io.IOException;
import java.io.InputStream;
import java.util.Optional;

@Service
public class TileResourceLoader {

    private final ObjectMapper objectMapper;

    public TileResourceLoader(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    public Optional<TileDefinition> load(String filePath) {
        ClassPathResource resource = new ClassPathResource(filePath);
        try (InputStream inputStream = resource.getInputStream()) {
            return Optional.of(objectMapper.readValue(inputStream, TileDefinition.class));
        } catch (IOException e) {
            unwrapAndThrowDomainUnchecked(e);
        }
        return Optional.empty();
    }

    private static void unwrapAndThrowDomainUnchecked(IOException e) {
        Throwable cause = e;
        while (cause != null) {
            if (cause instanceof TileDefinitionException tde) {
                throw tde;
            }
            cause = cause.getCause();
        }
        throw new RuntimeException(e);
    }
}